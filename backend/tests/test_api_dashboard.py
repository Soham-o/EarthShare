def test_dashboard_requires_onboarding_first(client, registered_user):
    headers, _, _ = registered_user
    resp = client.get("/api/v1/dashboard", headers=headers)
    assert resp.status_code == 404


def test_dashboard_returns_expected_shape(client, onboarded_user):
    headers, _, _ = onboarded_user
    resp = client.get("/api/v1/dashboard", headers=headers)
    assert resp.status_code == 200
    body = resp.json()
    for key in (
        "carbon_score",
        "total_kg_co2_month",
        "monthly_trend",
        "earthshare_dividend",
        "dividend_shares",
        "future_projection_kg_co2_year",
        "improved_projection_kg_co2_year",
        "top_emission_sources",
        "reduction_potential_kg_co2_month",
        "national_average_kg_co2_month",
    ):
        assert key in body
    assert body["dividend_shares"] >= 1
    assert len(body["top_emission_sources"]) <= 3


def test_completing_actions_increases_dividend(client, onboarded_user):
    headers, _, _ = onboarded_user
    before = client.get("/api/v1/dashboard", headers=headers).json()["earthshare_dividend"]

    actions = client.get("/api/v1/actions", headers=headers).json()
    client.post("/api/v1/actions/complete", headers=headers, json={"action_id": actions[0]["id"]})

    after = client.get("/api/v1/dashboard", headers=headers).json()["earthshare_dividend"]
    assert after > before


def test_top_emission_sources_sorted_descending(client, onboarded_user):
    headers, _, _ = onboarded_user
    body = client.get("/api/v1/dashboard", headers=headers).json()
    sources = body["top_emission_sources"]
    assert sources == sorted(sources, key=lambda s: s["kg_co2_month"], reverse=True)
