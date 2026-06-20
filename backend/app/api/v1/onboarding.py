from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.core.limiter import limiter
from app.models.user import User
from app.repositories.footprint_repository import FootprintRepository
from app.repositories.profile_repository import ProfileRepository
from app.schemas.footprint import FootprintSnapshot
from app.schemas.profile import OnboardingInput, ProfileResponse
from app.services.footprint_service import compute_and_record

router = APIRouter(prefix="/api/v1/onboarding", tags=["onboarding"])
_settings = get_settings()


@router.post("", response_model=FootprintSnapshot)
@limiter.limit(lambda: _settings.rate_limit_default)
def submit_onboarding(
    request: Request,
    payload: OnboardingInput,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    ProfileRepository(db).upsert(user_id=current_user.id, data=payload)
    record = compute_and_record(user_id=current_user.id, profile=payload, repo=FootprintRepository(db))
    return FootprintSnapshot(
        total_kg_co2_month=record.total_kg_co2_month,
        carbon_score=record.carbon_score,
        breakdown=record.breakdown_json["categories"],
        created_at=record.created_at,
    )


@router.get("/profile", response_model=ProfileResponse)
@limiter.limit(lambda: _settings.rate_limit_default)
def get_profile(request: Request, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    profile = ProfileRepository(db).get_by_user_id(current_user.id)
    if profile is None:
        from fastapi import HTTPException, status

        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Onboarding not completed yet.")
    return ProfileResponse.model_validate(profile)
