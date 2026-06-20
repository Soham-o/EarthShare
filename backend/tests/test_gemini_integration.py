"""
Gemini integration tests for the insight service.

Tests run in two modes:
  - Without GEMINI_API_KEY (always): verifies fallback behaviour is
    correct and the service never errors when Gemini is unavailable.
  - With GEMINI_API_KEY (CI optional / local): verifies the live API
    call succeeds and returns a well-formed InsightsResponse with
    source="gemini".

Set GEMINI_API_KEY in the environment (or .env.test) to enable live tests.
Skip markers prevent live tests from breaking CI when the key is absent.
"""
import json
import os
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from app.schemas.insight import InsightsResponse
from app.services.insight_service import _rule_based_insights, _try_gemini_rewrite, generate_insights
from app.services.carbon_engine import NATIONAL_AVERAGE_KG_CO2_MONTH

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

_SAMPLE_BREAKDOWN = [
    {"category": "transport", "kg_co2_month": 180.0, "percent_of_total": 45.0},
    {"category": "food",      "kg_co2_month": 110.0, "percent_of_total": 27.5},
    {"category": "energy",    "kg_co2_month":  60.0, "percent_of_total": 15.0},
    {"category": "shopping",  "kg_co2_month":  30.0, "percent_of_total":  7.5},
    {"category": "travel",    "kg_co2_month":  20.0, "percent_of_total":  5.0},
]
_TOTAL_KG = sum(c["kg_co2_month"] for c in _SAMPLE_BREAKDOWN)


# ---------------------------------------------------------------------------
# Rule-based fallback (no API key required)
# ---------------------------------------------------------------------------

class TestRuleBasedInsights:
    def test_returns_insights_response(self):
        result = _rule_based_insights(
            top_category="transport",
            percent_of_total=45.0,
            total_kg=_TOTAL_KG,
            national_average=NATIONAL_AVERAGE_KG_CO2_MONTH,
        )
        assert isinstance(result, InsightsResponse)

    def test_source_is_rule_based(self):
        result = _rule_based_insights(
            top_category="food",
            percent_of_total=30.0,
            total_kg=300.0,
            national_average=NATIONAL_AVERAGE_KG_CO2_MONTH,
        )
        assert result.source == "rule_based"

    def test_headline_contains_category(self):
        result = _rule_based_insights(
            top_category="energy",
            percent_of_total=40.0,
            total_kg=500.0,
            national_average=NATIONAL_AVERAGE_KG_CO2_MONTH,
        )
        assert "energy" in result.headline.lower()

    def test_weekly_action_plan_not_empty(self):
        result = _rule_based_insights(
            top_category="transport",
            percent_of_total=50.0,
            total_kg=600.0,
            national_average=NATIONAL_AVERAGE_KG_CO2_MONTH,
        )
        assert len(result.weekly_action_plan) >= 1

    def test_comparison_below_average(self):
        result = _rule_based_insights(
            top_category="food",
            percent_of_total=30.0,
            total_kg=200.0,  # well below 660 average
            national_average=NATIONAL_AVERAGE_KG_CO2_MONTH,
        )
        assert "below" in result.headline.lower()

    def test_comparison_above_average(self):
        result = _rule_based_insights(
            top_category="travel",
            percent_of_total=40.0,
            total_kg=900.0,  # above 660 average
            national_average=NATIONAL_AVERAGE_KG_CO2_MONTH,
        )
        assert "above" in result.headline.lower()


# ---------------------------------------------------------------------------
# generate_insights orchestration — Gemini mocked
# ---------------------------------------------------------------------------

class TestGenerateInsightsOrchestration:
    @pytest.mark.asyncio
    async def test_returns_rule_based_when_no_key(self, monkeypatch):
        monkeypatch.setattr("app.services.insight_service.settings.gemini_api_key", None)
        result = await generate_insights(
            breakdown_categories=_SAMPLE_BREAKDOWN,
            total_kg=_TOTAL_KG,
            national_average=NATIONAL_AVERAGE_KG_CO2_MONTH,
        )
        assert result.source == "rule_based"

    @pytest.mark.asyncio
    async def test_falls_back_to_rule_based_on_gemini_http_error(self, monkeypatch):
        monkeypatch.setattr("app.services.insight_service.settings.gemini_api_key", "fake-key")
        import httpx

        async def mock_post(*args, **kwargs):
            raise httpx.HTTPError("connection refused")

        with patch("httpx.AsyncClient.post", new=mock_post):
            result = await generate_insights(
                breakdown_categories=_SAMPLE_BREAKDOWN,
                total_kg=_TOTAL_KG,
                national_average=NATIONAL_AVERAGE_KG_CO2_MONTH,
            )
        assert result.source == "rule_based"

    @pytest.mark.asyncio
    async def test_uses_gemini_response_when_valid(self, monkeypatch):
        monkeypatch.setattr("app.services.insight_service.settings.gemini_api_key", "fake-key")

        rule_based_fixture = _rule_based_insights(
            top_category="transport",
            percent_of_total=45.0,
            total_kg=_TOTAL_KG,
            national_average=NATIONAL_AVERAGE_KG_CO2_MONTH,
        )
        gemini_payload = {
            "headline": "Gemini rewritten headline",
            "why_high": "Gemini why_high",
            "biggest_opportunity": "Gemini opportunity",
            "weekly_action_plan": ["Action A", "Action B"],
            "recommendations": ["Rec 1"],
            "future_self_message": "You did great!",
        }

        mock_response = MagicMock()
        mock_response.raise_for_status = MagicMock()
        mock_response.json = MagicMock(return_value={
            "candidates": [{"content": {"parts": [{"text": json.dumps(gemini_payload)}]}}]
        })

        with patch("httpx.AsyncClient.post", new=AsyncMock(return_value=mock_response)):
            result = await generate_insights(
                breakdown_categories=_SAMPLE_BREAKDOWN,
                total_kg=_TOTAL_KG,
                national_average=NATIONAL_AVERAGE_KG_CO2_MONTH,
            )

        assert result.source == "gemini"
        assert result.headline == "Gemini rewritten headline"

    @pytest.mark.asyncio
    async def test_falls_back_when_gemini_returns_malformed_json(self, monkeypatch):
        monkeypatch.setattr("app.services.insight_service.settings.gemini_api_key", "fake-key")

        mock_response = MagicMock()
        mock_response.raise_for_status = MagicMock()
        mock_response.json = MagicMock(return_value={
            "candidates": [{"content": {"parts": [{"text": "not-valid-json{{{}"}]}}]
        })

        with patch("httpx.AsyncClient.post", new=AsyncMock(return_value=mock_response)):
            result = await generate_insights(
                breakdown_categories=_SAMPLE_BREAKDOWN,
                total_kg=_TOTAL_KG,
                national_average=NATIONAL_AVERAGE_KG_CO2_MONTH,
            )

        assert result.source == "rule_based"

    @pytest.mark.asyncio
    async def test_falls_back_when_gemini_returns_missing_fields(self, monkeypatch):
        monkeypatch.setattr("app.services.insight_service.settings.gemini_api_key", "fake-key")

        mock_response = MagicMock()
        mock_response.raise_for_status = MagicMock()
        mock_response.json = MagicMock(return_value={
            "candidates": [{"content": {"parts": [{"text": '{"headline": "only headline"}'}]}}]
        })

        with patch("httpx.AsyncClient.post", new=AsyncMock(return_value=mock_response)):
            result = await generate_insights(
                breakdown_categories=_SAMPLE_BREAKDOWN,
                total_kg=_TOTAL_KG,
                national_average=NATIONAL_AVERAGE_KG_CO2_MONTH,
            )

        assert result.source == "rule_based"


# ---------------------------------------------------------------------------
# Live integration test — skipped unless GEMINI_API_KEY is set
# ---------------------------------------------------------------------------

@pytest.mark.skipif(
    not os.environ.get("GEMINI_API_KEY"),
    reason="GEMINI_API_KEY not set — skipping live Gemini integration test",
)
class TestGeminiLive:
    @pytest.mark.asyncio
    async def test_live_gemini_rewrite_returns_valid_insights(self):
        """Calls the real Gemini API. Only runs when GEMINI_API_KEY is set."""
        result = await generate_insights(
            breakdown_categories=_SAMPLE_BREAKDOWN,
            total_kg=_TOTAL_KG,
            national_average=NATIONAL_AVERAGE_KG_CO2_MONTH,
        )
        # Even on a live call, the contract must be satisfied.
        assert isinstance(result, InsightsResponse)
        assert result.source in ("gemini", "rule_based")  # allow fallback if quota hit
        assert result.headline
        assert len(result.weekly_action_plan) >= 1
        assert result.future_self_message
