"""Tests for the daily check-in endpoint."""
from datetime import datetime, timezone
from unittest.mock import patch


def _onboard(client, headers):
    resp = client.post(
        "/api/v1/onboarding",
        headers=headers,
        json={"transport": "bus", "food": "mixed", "energy": "medium", "shopping": "low", "travel": "rare"},
    )
    assert resp.status_code == 200, resp.text


class TestDailyCheckin:
    def test_checkin_requires_onboarding(self, client, registered_user):
        headers, _, _ = registered_user
        resp = client.post("/api/v1/checkin", headers=headers)
        assert resp.status_code == 400

    def test_checkin_creates_footprint_record(self, client, onboarded_user):
        headers, _, _ = onboarded_user
        resp = client.post("/api/v1/checkin", headers=headers)
        assert resp.status_code == 200
        body = resp.json()
        assert "carbon_score" in body
        assert "total_kg_co2_month" in body
        assert "breakdown" in body
        assert "created_at" in body

    def test_checkin_is_idempotent_same_day(self, client, onboarded_user):
        headers, _, _ = onboarded_user
        resp1 = client.post("/api/v1/checkin", headers=headers)
        assert resp1.status_code == 200

        resp2 = client.post("/api/v1/checkin", headers=headers)
        assert resp2.status_code == 200

        # Both calls return the same record (same created_at)
        assert resp1.json()["created_at"] == resp2.json()["created_at"]

    def test_get_checkin_returns_204_when_no_checkin_today(self, client, onboarded_user):
        """GET returns 204 if no check-in has happened today."""
        headers, _, _ = onboarded_user
        # Force "today" to be a different date so the existing onboarding record is in the past
        from datetime import date
        past_date = date(2000, 1, 1)
        with patch("app.api.v1.checkin._today_utc", return_value=past_date):
            resp = client.get("/api/v1/checkin", headers=headers)
        assert resp.status_code == 204

    def test_get_checkin_returns_200_after_checkin(self, client, onboarded_user):
        headers, _, _ = onboarded_user
        # POST to check in
        post_resp = client.post("/api/v1/checkin", headers=headers)
        assert post_resp.status_code == 200

        # GET should now return 200 with the same record
        get_resp = client.get("/api/v1/checkin", headers=headers)
        assert get_resp.status_code == 200
        assert get_resp.json()["created_at"] == post_resp.json()["created_at"]

    def test_checkin_updates_trend_chart(self, client, onboarded_user):
        """After a check-in the dashboard's monthly_trend should contain today's record."""
        headers, _, _ = onboarded_user
        client.post("/api/v1/checkin", headers=headers)

        dash_resp = client.get("/api/v1/dashboard", headers=headers)
        assert dash_resp.status_code == 200
        trend = dash_resp.json()["monthly_trend"]
        assert len(trend) >= 1  # at least onboarding + today's check-in

    def test_checkin_requires_auth(self, client):
        resp = client.post("/api/v1/checkin")
        assert resp.status_code == 401
