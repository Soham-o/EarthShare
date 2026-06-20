"""
Dashboard aggregation service.

Turns raw footprint history + completed actions into the product's core
"ownership" metaphor: a Carbon Score, an EarthShare Dividend, a forward
projection, and a ranked list of where the user's emissions actually come
from. All formulas here are intentionally simple linear functions of
already-computed inputs (no hidden ML, no external calls) so every number
on the dashboard is explainable in one sentence if a judge asks "how was
this calculated?" — see docs/CARBON_METHODOLOGY.md.
"""
from app.models.action import ACTION_CATALOG
from app.models.footprint import FootprintRecord
from app.schemas.footprint import (
    CategoryBreakdown,
    DashboardResponse,
    EmissionSource,
    FootprintSnapshot,
)
from app.services.carbon_engine import NATIONAL_AVERAGE_KG_CO2_MONTH

_CATEGORY_LABELS = {
    "transport": "Transport",
    "food": "Food",
    "energy": "Home energy",
    "shopping": "Shopping",
    "travel": "Long-distance travel",
}

# Dividend conversion: every kg of CO2/month saved versus the national
# average is worth this many dividend points. Arbitrary but fixed and
# documented — the point is consistency, not a "real" carbon price.
_DIVIDEND_POINTS_PER_KG_SAVED = 0.8

# A new share is issued for every N kg of cumulative CO2 saved through
# completed marketplace actions — this is what makes "shares" feel earned
# rather than just a relabeled score.
_KG_SAVED_PER_SHARE = 5.0


def _snapshot_from_record(record: FootprintRecord) -> FootprintSnapshot:
    breakdown = [CategoryBreakdown(**c) for c in record.breakdown_json["categories"]]
    return FootprintSnapshot(
        total_kg_co2_month=record.total_kg_co2_month,
        carbon_score=record.carbon_score,
        breakdown=breakdown,
        created_at=record.created_at,
    )


def build_dashboard(
    *, latest: FootprintRecord, history: list[FootprintRecord], completed_action_ids: set[str], total_kg_saved: float
) -> DashboardResponse:
    monthly_trend = [_snapshot_from_record(r) for r in history]

    kg_vs_average = NATIONAL_AVERAGE_KG_CO2_MONTH - latest.total_kg_co2_month
    dividend = round(max(0.0, kg_vs_average) * _DIVIDEND_POINTS_PER_KG_SAVED + total_kg_saved * 0.5, 2)
    shares = 1 + int(total_kg_saved // _KG_SAVED_PER_SHARE)

    categories = sorted(latest.breakdown_json["categories"], key=lambda c: c["kg_co2_month"], reverse=True)
    top_sources = [
        EmissionSource(
            category=c["category"],
            kg_co2_month=c["kg_co2_month"],
            label=f"{_CATEGORY_LABELS[c['category']]} — {c['percent_of_total']}% of your footprint",
        )
        for c in categories[:3]
    ]

    uncompleted = [a for a in ACTION_CATALOG if a.id not in completed_action_ids]
    reduction_potential = round(sum(a.kg_co2_saved_month for a in uncompleted), 2)

    top_two_savings = sum(a.kg_co2_saved_month for a in sorted(uncompleted, key=lambda a: a.kg_co2_saved_month, reverse=True)[:2])
    improved_monthly = max(0.0, latest.total_kg_co2_month - top_two_savings)

    return DashboardResponse(
        carbon_score=latest.carbon_score,
        total_kg_co2_month=latest.total_kg_co2_month,
        monthly_trend=monthly_trend,
        earthshare_dividend=dividend,
        dividend_shares=shares,
        future_projection_kg_co2_year=round(latest.total_kg_co2_month * 12, 1),
        improved_projection_kg_co2_year=round(improved_monthly * 12, 1),
        top_emission_sources=top_sources,
        reduction_potential_kg_co2_month=reduction_potential,
        national_average_kg_co2_month=NATIONAL_AVERAGE_KG_CO2_MONTH,
    )
