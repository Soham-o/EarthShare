import pytest

from app.schemas.profile import OnboardingInput
from app.services.carbon_engine import (
    SCORE_HIGH_ANCHOR_KG,
    SCORE_LOW_ANCHOR_KG,
    breakdown_dict,
    calculate_footprint,
)

LOW_IMPACT = OnboardingInput(transport="walking", food="vegetarian", energy="low", shopping="low", travel="rare")
HIGH_IMPACT = OnboardingInput(transport="car", food="meat_heavy", energy="high", shopping="high", travel="frequent")


def test_deterministic_for_identical_input():
    """Same input must always produce exactly the same output — the entire
    product narrative ('own a share of the planet') depends on this."""
    a = calculate_footprint(HIGH_IMPACT)
    b = calculate_footprint(HIGH_IMPACT)
    assert a == b


def test_total_is_sum_of_categories():
    result = calculate_footprint(HIGH_IMPACT)
    expected_total = round(
        result.transport_kg + result.food_kg + result.energy_kg + result.shopping_kg + result.travel_kg, 2
    )
    assert result.total_kg_co2_month == expected_total


def test_low_impact_profile_scores_higher_than_high_impact():
    low = calculate_footprint(LOW_IMPACT)
    high = calculate_footprint(HIGH_IMPACT)
    assert low.total_kg_co2_month < high.total_kg_co2_month
    assert low.carbon_score > high.carbon_score


@pytest.mark.parametrize("transport", ["car", "bus", "train", "bike", "walking"])
@pytest.mark.parametrize("food", ["vegetarian", "mixed", "meat_heavy"])
def test_all_known_category_combinations_calculate_without_error(transport, food):
    profile = OnboardingInput(transport=transport, food=food, energy="medium", shopping="medium", travel="monthly")
    result = calculate_footprint(profile)
    assert result.total_kg_co2_month > 0


def test_score_is_always_within_bounds():
    for profile in (LOW_IMPACT, HIGH_IMPACT):
        score = calculate_footprint(profile).carbon_score
        assert 0 <= score <= 1000


def test_score_anchors_are_sane():
    assert SCORE_LOW_ANCHOR_KG < SCORE_HIGH_ANCHOR_KG


def test_invalid_category_value_is_rejected_by_schema():
    with pytest.raises(Exception):
        OnboardingInput(transport="rocket_ship", food="mixed", energy="medium", shopping="medium", travel="rare")


def test_breakdown_percentages_sum_to_approximately_100():
    result = calculate_footprint(HIGH_IMPACT)
    breakdown = breakdown_dict(result)
    total_pct = sum(c["percent_of_total"] for c in breakdown["categories"])
    assert 99.0 <= total_pct <= 101.0  # rounding tolerance


def test_breakdown_contains_all_five_categories():
    result = calculate_footprint(LOW_IMPACT)
    breakdown = breakdown_dict(result)
    categories = {c["category"] for c in breakdown["categories"]}
    assert categories == {"transport", "food", "energy", "shopping", "travel"}
