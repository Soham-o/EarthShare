"""
Daily Check-In endpoint.

POST /api/v1/checkin  — idempotent, one footprint record per calendar day.
  - If the user has already checked in today (UTC), returns the existing record.
  - Otherwise re-runs the carbon engine against the saved profile and creates
    a new FootprintRecord, which automatically updates the trend charts.

GET  /api/v1/checkin  — returns today's check-in record if one exists (200)
    or 204 if the user has not yet checked in today.
"""
from datetime import date, datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.core.limiter import limiter
from app.models.user import User
from app.repositories.footprint_repository import FootprintRepository
from app.repositories.profile_repository import ProfileRepository
from app.schemas.footprint import FootprintSnapshot
from app.services.footprint_service import compute_and_record

router = APIRouter(prefix="/api/v1/checkin", tags=["checkin"])
_settings = get_settings()


def _today_utc() -> date:
    return datetime.now(timezone.utc).date()


def _find_todays_record(repo: FootprintRepository, user_id: str) -> FootprintSnapshot | None:
    """Return today's record if one already exists, else None."""
    today = _today_utc()
    # history() returns records newest-first (after the [::-1] reversal, actually oldest-first).
    # We only need to check the most recent record.
    latest = repo.latest(user_id)
    if latest is None:
        return None
    record_date = latest.created_at.astimezone(timezone.utc).date()
    if record_date == today:
        return FootprintSnapshot(
            total_kg_co2_month=latest.total_kg_co2_month,
            carbon_score=latest.carbon_score,
            breakdown=latest.breakdown_json["categories"],
            created_at=latest.created_at,
        )
    return None


@router.post("", response_model=FootprintSnapshot, status_code=status.HTTP_200_OK)
@limiter.limit(lambda: _settings.rate_limit_default)
def daily_checkin(
    request: Request,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Idempotent daily check-in. Returns an existing today's record if
    already present, or creates a fresh one from the saved profile."""
    repo = FootprintRepository(db)

    existing = _find_todays_record(repo, current_user.id)
    if existing:
        return existing

    # No check-in today — require onboarding to have been completed first.
    profile = ProfileRepository(db).get_by_user_id(current_user.id)
    if profile is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Complete onboarding before checking in.",
        )

    from app.schemas.profile import OnboardingInput

    payload = OnboardingInput(
        transport=profile.transport,
        food=profile.food,
        energy=profile.energy,
        shopping=profile.shopping,
        travel=profile.travel,
    )
    record = compute_and_record(user_id=current_user.id, profile=payload, repo=repo)
    return FootprintSnapshot(
        total_kg_co2_month=record.total_kg_co2_month,
        carbon_score=record.carbon_score,
        breakdown=record.breakdown_json["categories"],
        created_at=record.created_at,
    )


@router.get("", response_model=FootprintSnapshot, status_code=status.HTTP_200_OK)
@limiter.limit(lambda: _settings.rate_limit_default)
def get_todays_checkin(
    request: Request,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Returns today's check-in if one exists (200), or 204 No Content."""
    existing = _find_todays_record(FootprintRepository(db), current_user.id)
    if existing is None:
        from fastapi.responses import Response
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    return existing
