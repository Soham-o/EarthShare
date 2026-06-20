"""
Carbon Calculation Engine.

Deliberately local and rule-based: no external API call, no network
dependency, no nondeterminism. The same OnboardingInput always produces
the same output, which matters both for testability (see
tests/test_carbon_engine.py) and for user trust — a footprint score that
changes between two identical runs would undermine the entire "ownership"
metaphor the product is built on.

Emission factors below are simplified, order-of-magnitude figures derived
from widely published averages (EPA / Our World in Data style estimates
for an average-mileage commuter in a developed economy). They are
intentionally rounded for an MVP rule-based model, not a verified
lifecycle-assessment tool — see docs/CARBON_METHODOLOGY.md for the full
breakdown and the explicit assumptions behind each constant.
"""
from dataclasses import dataclass

from app.schemas.profile import OnboardingInput

# kg CO2e per month, per category level — see docs/CARBON_METHODOLOGY.md
TRANSPORT_FACTORS = {
    "car": 180.0,
    "bus": 70.0,
    "train": 45.0,
    "bike": 5.0,
    "walking": 2.0,
}

FOOD_FACTORS = {
    "vegetarian": 110.0,
    "mixed": 210.0,
    "meat_heavy": 290.0,
}

ENERGY_FACTORS = {
    "low": 60.0,
    "medium": 140.0,
    "high": 260.0,
}

SHOPPING_FACTORS = {
    "low": 30.0,
    "medium": 80.0,
    "high": 160.0,
}

# Flights/long-distance travel amortized to a monthly figure
TRAVEL_FACTORS = {
    "rare": 15.0,
    "monthly": 90.0,
    "frequent": 220.0,
}

# A commonly cited rough benchmark for an individual's monthly footprint in a
# developed economy, used only to contextualize a user's score (not part of
# the calculation itself).
NATIONAL_AVERAGE_KG_CO2_MONTH = 660.0

# Score calibration: a footprint at or below LOW_ANCHOR maps to score 1000;
# at or above HIGH_ANCHOR maps to score 0; linear in between. These anchors
# bound the realistic range produced by the factors above (min ~104,
# max ~930) with headroom on both ends.
SCORE_LOW_ANCHOR_KG = 150.0
SCORE_HIGH_ANCHOR_KG = 1000.0


@dataclass(frozen=True)
class FootprintResult:
    total_kg_co2_month: float
    transport_kg: float
    food_kg: float
    energy_kg: float
    shopping_kg: float
    travel_kg: float
    carbon_score: int


def calculate_footprint(profile: OnboardingInput) -> FootprintResult:
    transport_kg = TRANSPORT_FACTORS[profile.transport]
    food_kg = FOOD_FACTORS[profile.food]
    energy_kg = ENERGY_FACTORS[profile.energy]
    shopping_kg = SHOPPING_FACTORS[profile.shopping]
    travel_kg = TRAVEL_FACTORS[profile.travel]

    total = round(transport_kg + food_kg + energy_kg + shopping_kg + travel_kg, 2)
    score = _score_from_total(total)

    return FootprintResult(
        total_kg_co2_month=total,
        transport_kg=transport_kg,
        food_kg=food_kg,
        energy_kg=energy_kg,
        shopping_kg=shopping_kg,
        travel_kg=travel_kg,
        carbon_score=score,
    )


def _score_from_total(total_kg: float) -> int:
    """Maps kg CO2/month to a 0-1000 score, higher is better (less carbon).
    Clamped and linear between the calibration anchors — simple, explainable,
    and monotonic, which matters more for an MVP than a more 'accurate' but
    opaque curve."""
    span = SCORE_HIGH_ANCHOR_KG - SCORE_LOW_ANCHOR_KG
    clamped = max(SCORE_LOW_ANCHOR_KG, min(SCORE_HIGH_ANCHOR_KG, total_kg))
    fraction_bad = (clamped - SCORE_LOW_ANCHOR_KG) / span
    return round(1000 * (1 - fraction_bad))


def breakdown_dict(result: FootprintResult) -> dict:
    categories = {
        "transport": result.transport_kg,
        "food": result.food_kg,
        "energy": result.energy_kg,
        "shopping": result.shopping_kg,
        "travel": result.travel_kg,
    }
    total = result.total_kg_co2_month or 1  # guard div-by-zero, total is always > 0 in practice
    return {
        "categories": [
            {
                "category": name,
                "kg_co2_month": value,
                "percent_of_total": round(100 * value / total, 1),
            }
            for name, value in categories.items()
        ]
    }
