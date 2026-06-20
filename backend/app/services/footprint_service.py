from app.models.footprint import FootprintRecord
from app.repositories.footprint_repository import FootprintRepository
from app.schemas.profile import OnboardingInput
from app.services.carbon_engine import breakdown_dict, calculate_footprint


def compute_and_record(*, user_id: str, profile: OnboardingInput, repo: FootprintRepository) -> FootprintRecord:
    result = calculate_footprint(profile)
    breakdown = breakdown_dict(result)
    return repo.create(
        user_id=user_id,
        total_kg_co2_month=result.total_kg_co2_month,
        transport_kg=result.transport_kg,
        food_kg=result.food_kg,
        energy_kg=result.energy_kg,
        shopping_kg=result.shopping_kg,
        travel_kg=result.travel_kg,
        carbon_score=result.carbon_score,
        breakdown_json=breakdown,
    )
