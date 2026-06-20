def test_onboarding_requires_auth(client):
    resp = client.post(
        "/api/v1/onboarding",
        json={"transport": "car", "food": "mixed", "energy": "medium", "shopping": "medium", "travel": "rare"},
    )
    assert resp.status_code == 401


def test_onboarding_rejects_invalid_enum_value(client, registered_user):
    headers, _, _ = registered_user
    resp = client.post(
        "/api/v1/onboarding",
        headers=headers,
        json={"transport": "spaceship", "food": "mixed", "energy": "medium", "shopping": "medium", "travel": "rare"},
    )
    assert resp.status_code == 422


def test_onboarding_creates_footprint_snapshot(client, registered_user):
    headers, _, _ = registered_user
    resp = client.post(
        "/api/v1/onboarding",
        headers=headers,
        json={"transport": "bike", "food": "vegetarian", "energy": "low", "shopping": "low", "travel": "rare"},
    )
    assert resp.status_code == 200
    body = resp.json()
    assert body["total_kg_co2_month"] > 0
    assert 0 <= body["carbon_score"] <= 1000
    assert len(body["breakdown"]) == 5


def test_profile_not_found_before_onboarding(client, registered_user):
    headers, _, _ = registered_user
    resp = client.get("/api/v1/onboarding/profile", headers=headers)
    assert resp.status_code == 404


def test_profile_returned_after_onboarding(client, onboarded_user):
    headers, _, _ = onboarded_user
    resp = client.get("/api/v1/onboarding/profile", headers=headers)
    assert resp.status_code == 200
    assert resp.json()["transport"] == "car"


def test_resubmitting_onboarding_updates_profile_and_adds_history(client, onboarded_user):
    headers, _, _ = onboarded_user
    resp = client.post(
        "/api/v1/onboarding",
        headers=headers,
        json={"transport": "walking", "food": "vegetarian", "energy": "low", "shopping": "low", "travel": "rare"},
    )
    assert resp.status_code == 200
    profile = client.get("/api/v1/onboarding/profile", headers=headers).json()
    assert profile["transport"] == "walking"

    dashboard = client.get("/api/v1/dashboard", headers=headers).json()
    assert len(dashboard["monthly_trend"]) == 2  # original high-impact + the update
