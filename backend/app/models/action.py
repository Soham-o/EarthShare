"""
Action Marketplace catalog.

This is reference data, not user data — every user sees the same catalog,
so it lives as a typed in-memory constant rather than a database table.
That keeps the marketplace deterministic and avoids a migration just to
ship six rows. (If this grows into something admin-editable, promote it
to a table + repository at that point — see services/action_service.py
for where that seam already lives.)
"""
from dataclasses import dataclass
from typing import Literal

Difficulty = Literal["easy", "medium", "hard"]


@dataclass(frozen=True)
class MarketplaceAction:
    id: str
    title: str
    description: str
    category: Literal["transport", "food", "energy", "shopping", "travel"]
    kg_co2_saved_month: float
    difficulty: Difficulty
    impact_score: int  # 1-100, relative scale for sorting/badging


ACTION_CATALOG: list[MarketplaceAction] = [
    MarketplaceAction(
        id="use_public_transport",
        title="Use public transport twice a week",
        description="Swap two car trips a week for bus or train.",
        category="transport",
        kg_co2_saved_month=18.0,
        difficulty="easy",
        impact_score=70,
    ),
    MarketplaceAction(
        id="reduce_food_waste",
        title="Cut food waste",
        description="Plan meals and store leftovers to stop edible food going to landfill.",
        category="food",
        kg_co2_saved_month=10.0,
        difficulty="easy",
        impact_score=55,
    ),
    MarketplaceAction(
        id="buy_local_products",
        title="Buy local, seasonal produce",
        description="Choose local produce over goods shipped long distance.",
        category="shopping",
        kg_co2_saved_month=8.0,
        difficulty="medium",
        impact_score=45,
    ),
    MarketplaceAction(
        id="turn_off_idle_devices",
        title="Turn off idle devices",
        description="Switch off devices and chargers fully instead of leaving them on standby.",
        category="energy",
        kg_co2_saved_month=6.0,
        difficulty="easy",
        impact_score=40,
    ),
    MarketplaceAction(
        id="reduce_meat_consumption",
        title="Go meat-free two days a week",
        description="Replace two meat meals a week with plant-based alternatives.",
        category="food",
        kg_co2_saved_month=22.0,
        difficulty="medium",
        impact_score=80,
    ),
    MarketplaceAction(
        id="carpool_to_work",
        title="Carpool twice a week",
        description="Share rides with a colleague or neighbour for two commutes a week.",
        category="transport",
        kg_co2_saved_month=14.0,
        difficulty="medium",
        impact_score=60,
    ),
]


def get_action(action_id: str) -> MarketplaceAction | None:
    return next((a for a in ACTION_CATALOG if a.id == action_id), None)
