from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.core.limiter import limiter
from app.models.user import User
from app.repositories.footprint_repository import ActionCompletionRepository, FootprintRepository
from app.schemas.insight import ProgressResponse
from app.services.action_service import build_progress

router = APIRouter(prefix="/api/v1/progress", tags=["progress"])
_settings = get_settings()


@router.get("", response_model=ProgressResponse)
@limiter.limit(lambda: _settings.rate_limit_default)
def get_progress(request: Request, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    data = build_progress(
        user_id=current_user.id,
        footprint_repo=FootprintRepository(db),
        action_repo=ActionCompletionRepository(db),
    )
    return ProgressResponse(**data)
