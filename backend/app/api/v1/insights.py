from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.core.limiter import limiter
from app.models.user import User
from app.repositories.footprint_repository import FootprintRepository
from app.schemas.insight import InsightsResponse
from app.services.carbon_engine import NATIONAL_AVERAGE_KG_CO2_MONTH
from app.services.insight_service import generate_insights

router = APIRouter(prefix="/api/v1/insights", tags=["insights"])
_settings = get_settings()


@router.get("", response_model=InsightsResponse)
@limiter.limit(lambda: _settings.rate_limit_default)
async def get_insights(request: Request, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    latest = FootprintRepository(db).latest(current_user.id)
    if latest is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Complete onboarding first to generate insights.",
        )

    return await generate_insights(
        breakdown_categories=latest.breakdown_json["categories"],
        total_kg=latest.total_kg_co2_month,
        national_average=NATIONAL_AVERAGE_KG_CO2_MONTH,
    )
