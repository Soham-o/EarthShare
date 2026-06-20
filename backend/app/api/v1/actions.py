from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.core.limiter import limiter
from app.models.user import User
from app.repositories.footprint_repository import ActionCompletionRepository
from app.schemas.insight import ActionCardResponse, ActionCompletionRequest
from app.services.action_service import ActionAlreadyCompleted, UnknownAction, complete_action, list_action_cards

router = APIRouter(prefix="/api/v1/actions", tags=["actions"])
_settings = get_settings()


@router.get("", response_model=list[ActionCardResponse])
@limiter.limit(lambda: _settings.rate_limit_default)
def get_actions(request: Request, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    completions = ActionCompletionRepository(db).list_for_user(current_user.id)
    return list_action_cards(completions)


@router.post("/complete", status_code=status.HTTP_201_CREATED)
@limiter.limit(lambda: _settings.rate_limit_default)
def complete(
    request: Request,
    payload: ActionCompletionRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    try:
        complete_action(user_id=current_user.id, action_id=payload.action_id, repo=ActionCompletionRepository(db))
    except UnknownAction as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))
    except ActionAlreadyCompleted as exc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc))
    return {"status": "completed"}
