"""Action marketplace and progress/badges logic. Badges are computed, not
stored — they're a pure function of completion history, so there's no risk
of badge state drifting out of sync with the underlying data."""
from app.models.action import ACTION_CATALOG, get_action
from app.models.footprint import ActionCompletion
from app.repositories.footprint_repository import ActionCompletionRepository, FootprintRepository
from app.schemas.insight import ActionCardResponse, BadgeResponse

_BADGE_DEFS = [
    {"id": "first_step", "title": "First Step", "description": "Completed your first action.", "threshold": 1},
    {"id": "habit_builder", "title": "Habit Builder", "description": "Completed 3 actions.", "threshold": 3},
    {"id": "earthshare_champion", "title": "EarthShare Champion", "description": "Completed all 6 actions.", "threshold": 6},
]


class ActionAlreadyCompleted(Exception):
    pass


class UnknownAction(Exception):
    pass


def list_action_cards(completions: list[ActionCompletion]) -> list[ActionCardResponse]:
    completed_ids = {c.action_id for c in completions}
    return [
        ActionCardResponse(
            id=a.id,
            title=a.title,
            description=a.description,
            category=a.category,
            kg_co2_saved_month=a.kg_co2_saved_month,
            difficulty=a.difficulty,
            impact_score=a.impact_score,
            completed=a.id in completed_ids,
        )
        for a in ACTION_CATALOG
    ]


def complete_action(*, user_id: str, action_id: str, repo: ActionCompletionRepository) -> ActionCompletion:
    action = get_action(action_id)
    if action is None:
        raise UnknownAction(f"No such action: {action_id}")
    if repo.get(user_id, action_id) is not None:
        raise ActionAlreadyCompleted("This action is already marked complete.")
    return repo.create(user_id=user_id, action_id=action_id, kg_co2_saved=action.kg_co2_saved_month)


def compute_badges(completions: list[ActionCompletion]) -> list[BadgeResponse]:
    count = len(completions)
    return [
        BadgeResponse(id=b["id"], title=b["title"], description=b["description"], earned=count >= b["threshold"])
        for b in _BADGE_DEFS
    ]


def build_progress(*, user_id: str, footprint_repo: FootprintRepository, action_repo: ActionCompletionRepository):
    history = footprint_repo.history(user_id, limit=12)
    completions = action_repo.list_for_user(user_id)

    weekly_trend = [
        {"date": r.created_at.isoformat(), "carbon_score": r.carbon_score, "total_kg_co2_month": r.total_kg_co2_month}
        for r in history
    ]

    return {
        "weekly_trend": weekly_trend,
        "badges": [b.model_dump() for b in compute_badges(completions)],
        "total_actions_completed": len(completions),
        "total_kg_co2_saved": round(sum(c.kg_co2_saved for c in completions), 2),
    }
