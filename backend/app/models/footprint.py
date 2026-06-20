from datetime import datetime, timezone

from sqlalchemy import DateTime, Float, ForeignKey, JSON, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.models.user import _uuid


class FootprintRecord(Base):
    """A point-in-time snapshot of a user's calculated footprint. One row is
    written every time the carbon engine runs (onboarding completion, profile
    update, or the daily recompute), which is what powers the trend chart and
    the dividend/projection math without needing to re-derive history."""

    __tablename__ = "footprint_records"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=_uuid)
    user_id: Mapped[str] = mapped_column(String, ForeignKey("users.id"), index=True, nullable=False)

    total_kg_co2_month: Mapped[float] = mapped_column(Float, nullable=False)
    transport_kg: Mapped[float] = mapped_column(Float, nullable=False)
    food_kg: Mapped[float] = mapped_column(Float, nullable=False)
    energy_kg: Mapped[float] = mapped_column(Float, nullable=False)
    shopping_kg: Mapped[float] = mapped_column(Float, nullable=False)
    travel_kg: Mapped[float] = mapped_column(Float, nullable=False)

    carbon_score: Mapped[int] = mapped_column(nullable=False)  # 0-1000, higher = better
    breakdown_json: Mapped[dict] = mapped_column(JSON, nullable=False)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    user = relationship("User", back_populates="footprint_records")


class ActionCompletion(Base):
    """Tracks which marketplace actions a user has marked complete, and when —
    drives both the dividend boost and the achievement badges."""

    __tablename__ = "action_completions"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=_uuid)
    user_id: Mapped[str] = mapped_column(String, ForeignKey("users.id"), index=True, nullable=False)
    action_id: Mapped[str] = mapped_column(String, nullable=False)
    kg_co2_saved: Mapped[float] = mapped_column(Float, nullable=False)
    completed_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    user = relationship("User", back_populates="action_completions")
