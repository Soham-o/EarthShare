from app.core.security import create_access_token


def test_security_headers_present_on_every_response(client):
    resp = client.get("/health")
    assert resp.headers["X-Content-Type-Options"] == "nosniff"
    assert resp.headers["X-Frame-Options"] == "DENY"
    assert "Referrer-Policy" in resp.headers
    assert "Permissions-Policy" in resp.headers


def test_health_check_does_not_require_auth(client):
    resp = client.get("/health")
    assert resp.status_code == 200


def test_tampered_jwt_signature_is_rejected(client):
    token = create_access_token(subject="some-user-id")
    tampered = token[:-4] + "abcd"  # corrupt the signature
    resp = client.get("/api/v1/auth/me", headers={"Authorization": f"Bearer {tampered}"})
    assert resp.status_code == 401


def test_jwt_for_nonexistent_user_is_rejected(client):
    token = create_access_token(subject="user-id-that-was-never-created")
    resp = client.get("/api/v1/auth/me", headers={"Authorization": f"Bearer {token}"})
    assert resp.status_code == 401


def test_expired_token_is_rejected(client):
    import datetime

    token = create_access_token(subject="some-user-id", expires_delta=datetime.timedelta(seconds=-1))
    resp = client.get("/api/v1/auth/me", headers={"Authorization": f"Bearer {token}"})
    assert resp.status_code == 401


def test_register_endpoint_is_rate_limited(client):
    last_status = None
    for i in range(15):
        last_status = client.post(
            "/api/v1/auth/register",
            json={"email": f"rl{i}@example.com", "full_name": "Rate Limited", "password": "Passw0rd1"},
        ).status_code
    assert last_status == 429


def test_sql_injection_style_email_is_handled_safely(client):
    """The ORM parameterizes everything, so this should just behave like a
    normal (failed) login — not throw, not leak a DB error."""
    resp = client.post(
        "/api/v1/auth/login",
        json={"email": "not-an-email", "password": "x' OR '1'='1"},
    )
    assert resp.status_code == 422  # rejected by EmailStr validation, well before any query runs


def test_unhandled_error_does_not_leak_internals(monkeypatch):
    from fastapi.testclient import TestClient

    from app.api.v1 import dashboard as dashboard_route
    from app.main import app

    def _boom(**kwargs):
        raise RuntimeError("simulated internal failure with a secret stack trace")

    monkeypatch.setattr(dashboard_route, "build_dashboard", _boom)

    # raise_server_exceptions=False: we want to assert on the HTTP response
    # our own handler produces, not have the test runner re-raise the
    # exception past it.
    client = TestClient(app, raise_server_exceptions=False)

    # Need an onboarded user to reach the code path that calls build_dashboard.
    reg = client.post(
        "/api/v1/auth/register",
        json={"email": "leaktest@example.com", "full_name": "Leak Test", "password": "Passw0rd1"},
    ).json()
    headers = {"Authorization": f"Bearer {reg['access_token']}"}
    client.post(
        "/api/v1/onboarding",
        headers=headers,
        json={"transport": "car", "food": "mixed", "energy": "medium", "shopping": "medium", "travel": "rare"},
    )

    resp = client.get("/api/v1/dashboard", headers=headers)
    assert resp.status_code == 500
    assert "secret stack trace" not in resp.text
    assert resp.json() == {"detail": "Internal server error."}
