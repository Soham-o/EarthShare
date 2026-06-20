def test_register_returns_token(client):
    resp = client.post(
        "/api/v1/auth/register",
        json={"email": "new@example.com", "full_name": "Grace Hopper", "password": "Compil3rs"},
    )
    assert resp.status_code == 201
    assert "access_token" in resp.json()


def test_register_rejects_weak_password(client):
    resp = client.post(
        "/api/v1/auth/register",
        json={"email": "weak@example.com", "full_name": "Weak Pw", "password": "short"},
    )
    assert resp.status_code == 422


def test_register_rejects_duplicate_email(client):
    payload = {"email": "dupe@example.com", "full_name": "First User", "password": "Passw0rd1"}
    first = client.post("/api/v1/auth/register", json=payload)
    assert first.status_code == 201
    second = client.post("/api/v1/auth/register", json=payload)
    assert second.status_code == 409


def test_login_succeeds_with_correct_credentials(client):
    client.post(
        "/api/v1/auth/register",
        json={"email": "loginme@example.com", "full_name": "Login Me", "password": "Passw0rd1"},
    )
    resp = client.post("/api/v1/auth/login", json={"email": "loginme@example.com", "password": "Passw0rd1"})
    assert resp.status_code == 200
    assert "access_token" in resp.json()


def test_login_fails_with_wrong_password(client):
    client.post(
        "/api/v1/auth/register",
        json={"email": "wrongpw@example.com", "full_name": "Wrong Pw", "password": "Passw0rd1"},
    )
    resp = client.post("/api/v1/auth/login", json={"email": "wrongpw@example.com", "password": "NotTheRight1"})
    assert resp.status_code == 401


def test_login_fails_for_unknown_email(client):
    resp = client.post("/api/v1/auth/login", json={"email": "ghost@example.com", "password": "Whatever1"})
    assert resp.status_code == 401


def test_me_requires_authentication(client):
    resp = client.get("/api/v1/auth/me")
    assert resp.status_code == 401


def test_me_rejects_garbage_token(client):
    resp = client.get("/api/v1/auth/me", headers={"Authorization": "Bearer not-a-real-token"})
    assert resp.status_code == 401


def test_me_returns_profile_for_valid_token(client, registered_user):
    headers, email, _ = registered_user
    resp = client.get("/api/v1/auth/me", headers=headers)
    assert resp.status_code == 200
    assert resp.json()["email"] == email
    assert resp.json()["has_completed_onboarding"] is False


def test_me_reflects_onboarding_state(client, onboarded_user):
    headers, email, _ = onboarded_user
    resp = client.get("/api/v1/auth/me", headers=headers)
    assert resp.status_code == 200
    body = resp.json()
    assert body["email"] == email
    assert body["has_completed_onboarding"] is True


def test_password_is_never_stored_in_plaintext():
    from app.core.security import hash_password

    hashed = hash_password("Passw0rd1")
    assert hashed != "Passw0rd1"
    assert hashed.startswith("$2b$")
