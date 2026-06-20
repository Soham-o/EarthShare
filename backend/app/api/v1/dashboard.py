from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.core.limiter import limiter
from app.models.user import User
from app.repositories.footprint_repository import ActionCompletionRepository, FootprintRepository
from app.schemas.footprint import DashboardResponse
from app.services.dashboard_service import build_dashboard

router = APIRouter(prefix="/api/v1/dashboard", tags=["dashboard"])
_settings = get_settings()


@router.get("", response_model=DashboardResponse)
@limiter.limit(lambda: _settings.rate_limit_default)
def get_dashboard(request: Request, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    footprint_repo = FootprintRepository(db)
    latest = footprint_repo.latest(current_user.id)
    if latest is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Complete onboarding first to generate your dashboard.",
        )

    history = footprint_repo.history(current_user.id, limit=12)
    completions = ActionCompletionRepository(db).list_for_user(current_user.id)

    return build_dashboard(
        latest=latest,
        history=history,
        completed_action_ids={c.action_id for c in completions},
        total_kg_saved=sum(c.kg_co2_saved for c in completions),
    )
