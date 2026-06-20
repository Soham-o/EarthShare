from sqlalchemy.orm import Session

from app.models.profile import CarbonProfile
from app.schemas.profile import OnboardingInput


class ProfileRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_user_id(self, user_id: str) -> CarbonProfile | None:
        return self.db.query(CarbonProfile).filter(CarbonProfile.user_id == user_id).first()

    def upsert(self, *, user_id: str, data: OnboardingInput) -> CarbonProfile:
        profile = self.get_by_user_id(user_id)
        if profile is None:
            profile = CarbonProfile(user_id=user_id, **data.model_dump())
            self.db.add(profile)
        else:
            for field, value in data.model_dump().items():
                setattr(profile, field, value)
        self.db.commit()
        self.db.refresh(profile)
        return profile
