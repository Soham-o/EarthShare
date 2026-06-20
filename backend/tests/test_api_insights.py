def test_insights_requires_onboarding_first(client, registered_user):
    headers, _, _ = registered_user
    resp = client.get("/api/v1/insights", headers=headers)
    assert resp.status_code == 404


def test_insights_returns_rule_based_without_gemini_key(client, onboarded_user):
    headers, _, _ = onboarded_user
    resp = client.get("/api/v1/insights", headers=headers)
    assert resp.status_code == 200
    body = resp.json()
    assert body["source"] == "rule_based"
    assert body["headline"]
    assert len(body["weekly_action_plan"]) >= 1
    assert "future self" in body["future_self_message"].lower() or body["future_self_message"]


def test_insights_mentions_dominant_category(client, registered_user):
    headers, _, _ = registered_user
    client.post(
        "/api/v1/onboarding",
        headers=headers,
        json={"transport": "car", "food": "vegetarian", "energy": "low", "shopping": "low", "travel": "rare"},
    )
    body = client.get("/api/v1/insights", headers=headers).json()
    assert "transport" in body["headline"].lower() or "transport" in body["why_high"].lower()
