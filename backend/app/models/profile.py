from datetime import datetime, timezone

from sqlalchemy import DateTime, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.models.user import _uuid


class CarbonProfile(Base):
    """Stores the answers from Smart Carbon Onboarding. One profile per user;
    re-running onboarding updates this row (and the change is captured as a
    new FootprintRecord so trend history is preserved)."""

    __tablename__ = "carbon_profiles"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=_uuid)
    user_id: Mapped[str] = mapped_column(String, ForeignKey("users.id"), unique=True, nullable=False)

    transport: Mapped[str] = mapped_column(String, nullable=False)  # car|bike|bus|train|walking
    food: Mapped[str] = mapped_column(String, nullable=False)  # vegetarian|mixed|meat_heavy
    energy: Mapped[str] = mapped_column(String, nullable=False)  # low|medium|high
    shopping: Mapped[str] = mapped_column(String, nullable=False)  # low|medium|high
    travel: Mapped[str] = mapped_column(String, nullable=False)  # rare|monthly|frequent

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc)
    )

    user = relationship("User", back_populates="profile")
