import os
import uuid

os.environ["DATABASE_URL"] = "sqlite:///:memory:"
os.environ["JWT_SECRET_KEY"] = "test-secret-key-not-for-production"
os.environ["ENVIRONMENT"] = "test"

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.core.database import Base, get_db
from app.core.limiter import limiter
from app.main import app

# A single shared in-memory SQLite connection for the whole test session,
# via StaticPool — this is what makes ":memory:" usable across the
# multiple connections FastAPI's dependency injection opens per request.
_engine = create_engine(
    "sqlite:///:memory:",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
_TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=_engine)


@pytest.fixture(scope="session", autouse=True)
def _create_test_schema():
    Base.metadata.create_all(bind=_engine)
    yield
    Base.metadata.drop_all(bind=_engine)


@pytest.fixture(autouse=True)
def _reset_rate_limiter():
    """Rate limits are keyed by client IP, and TestClient always uses the
    same fake IP — without a reset, the auth-test suite alone would trip
    the 10/minute limit and fail unrelated tests."""
    limiter.reset()
    yield


def _override_get_db():
    db = _TestSessionLocal()
    try:
        yield db
        db.commit()
    finally:
        db.close()


app.dependency_overrides[get_db] = _override_get_db


@pytest.fixture()
def client():
    with TestClient(app) as c:
        yield c
    # Clean tables between tests so each test starts from a known state.
    with _engine.begin() as conn:
        for table in reversed(Base.metadata.sorted_tables):
            conn.execute(table.delete())


@pytest.fixture()
def registered_user(client):
    """Registers a fresh user and returns (auth_headers, email, password)."""
    email = f"{uuid.uuid4().hex[:10]}@example.com"
    password = "Sup3rSecret"
    resp = client.post(
        "/api/v1/auth/register",
        json={"email": email, "full_name": "Ada Lovelace", "password": password},
    )
    assert resp.status_code == 201, resp.text
    token = resp.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}, email, password


@pytest.fixture()
def onboarded_user(client, registered_user):
    """Like registered_user, but has also completed onboarding."""
    headers, email, password = registered_user
    resp = client.post(
        "/api/v1/onboarding",
        headers=headers,
        json={"transport": "car", "food": "meat_heavy", "energy": "high", "shopping": "high", "travel": "frequent"},
    )
    assert resp.status_code == 200, resp.text
    return headers, email, password
