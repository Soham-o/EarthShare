"""
SQLAlchemy engine/session wiring.

Built against the ORM layer only — no SQLite-specific or Postgres-specific
SQL anywhere in models/repositories — so switching DATABASE_URL to a
Postgres DSN is the only change required to move environments.
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

from app.core.config import get_settings

settings = get_settings()

connect_args = {"check_same_thread": False} if settings.database_url.startswith("sqlite") else {}

engine = create_engine(settings.database_url, connect_args=connect_args)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    pass


def get_db() -> Session:
    """FastAPI dependency: yields a request-scoped DB session and always closes it."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db() -> None:
    """Create tables. For an MVP this replaces a full migration pipeline;
    swap for Alembic migrations before any production deployment."""
    from app.models import action, footprint, profile, user  # noqa: F401  (registers metadata)

    Base.metadata.create_all(bind=engine)
