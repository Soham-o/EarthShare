"""
Personalized AI Insights.

Design choice: a deterministic rule-based generator is the source of
truth, and Gemini (if GEMINI_API_KEY is configured) is used only to
rewrite that same structured content in a more natural voice. This means:

  1. The feature works with zero configuration and zero internet access —
     important for a live demo where API quota or network can't be
     guaranteed.
  2. The numbers in the insight (percentages, projected savings) are
     always computed by the carbon engine, never hallucinated by the
     model — Gemini is asked to phrase, not to calculate.
  3. Any Gemini failure (timeout, auth, rate limit) falls back silently
     to the rule-based text rather than breaking the dashboard.
"""
import httpx

from app.core.config import get_settings
from app.models.action import ACTION_CATALOG
from app.schemas.insight import InsightsResponse

settings = get_settings()

_CATEGORY_TIPS = {
    "transport": "Two car trips a week swapped for public transport or carpooling is the single biggest lever here.",
    "food": "Cutting back on meat-heavy meals a couple of times a week moves this number more than almost anything else.",
    "energy": "Idle devices and heating/cooling habits are the easiest wins in this category.",
    "shopping": "Buying less, and choosing local or secondhand where possible, reduces this category fastest.",
    "travel": "Long-distance trips dominate this category — even one fewer flight a year has an outsized effect.",
}


def _rule_based_insights(*, top_category: str, percent_of_total: float, total_kg: float, national_average: float) -> InsightsResponse:
    diff_pct = round(100 * (total_kg - national_average) / national_average, 0)
    comparison = (
        f"about {abs(diff_pct):.0f}% below the typical average" if diff_pct < 0
        else f"about {diff_pct:.0f}% above the typical average" if diff_pct > 0
        else "right at the typical average"
    )

    relevant_actions = sorted(
        (a for a in ACTION_CATALOG if a.category == top_category),
        key=lambda a: a.kg_co2_saved_month,
        reverse=True,
    )[:2] or sorted(ACTION_CATALOG, key=lambda a: a.kg_co2_saved_month, reverse=True)[:2]

    weekly_plan = [f"{a.title} — saves roughly {a.kg_co2_saved_month:.0f} kg CO2/month" for a in relevant_actions]

    return InsightsResponse(
        headline=f"Your footprint is currently {comparison}, driven mainly by {top_category}.",
        why_high=(
            f"{top_category.capitalize()} makes up {percent_of_total:.0f}% of your monthly footprint — "
            f"the largest single category. {_CATEGORY_TIPS.get(top_category, '')}"
        ),
        biggest_opportunity=(
            f"Focusing on {top_category} gives you the fastest path down: it's where you have the most "
            f"room to improve relative to its size."
        ),
        weekly_action_plan=weekly_plan,
        recommendations=[a.description for a in relevant_actions],
        future_self_message="Your future self thanks you for reducing unnecessary travel this month."
        if top_category in ("transport", "travel")
        else "Your future self thanks you for the small changes you're making today.",
        source="rule_based",
    )


async def _try_gemini_rewrite(rule_based: InsightsResponse) -> InsightsResponse | None:
    if not settings.gemini_api_key:
        return None

    prompt = (
        "Rewrite the following carbon-footprint insight in a warm, encouraging, concise voice. "
        "Keep every number exactly as given — do not invent or change any figure. "
        "Return ONLY a JSON object with keys: headline, why_high, biggest_opportunity, "
        "weekly_action_plan (array of strings), recommendations (array of strings), future_self_message.\n\n"
        f"Source data: {rule_based.model_dump_json(exclude={'source'})}"
    )

    url = (
        f"https://generativelanguage.googleapis.com/v1beta/models/"
        f"{settings.gemini_model}:generateContent?key={settings.gemini_api_key}"
    )

    try:
        async with httpx.AsyncClient(timeout=6.0) as client:
            resp = await client.post(url, json={"contents": [{"parts": [{"text": prompt}]}]})
            resp.raise_for_status()
            data = resp.json()
            text = data["candidates"][0]["content"]["parts"][0]["text"]
            text = text.strip().removeprefix("```json").removeprefix("```").removesuffix("```").strip()
            import json

            parsed = json.loads(text)
            return InsightsResponse(**parsed, source="gemini")
    except Exception:
        # Any failure (network, auth, parsing, quota) — silently keep the
        # rule-based result. This is a UX enhancement, never a dependency.
        return None


async def generate_insights(
    *, breakdown_categories: list[dict], total_kg: float, national_average: float
) -> InsightsResponse:
    top = max(breakdown_categories, key=lambda c: c["kg_co2_month"])
    rule_based = _rule_based_insights(
        top_category=top["category"],
        percent_of_total=top["percent_of_total"],
        total_kg=total_kg,
        national_average=national_average,
    )

    enhanced = await _try_gemini_rewrite(rule_based)
    return enhanced or rule_based
