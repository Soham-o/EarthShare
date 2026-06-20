from typing import Literal

from pydantic import BaseModel

TransportType = Literal["car", "bike", "bus", "train", "walking"]
FoodType = Literal["vegetarian", "mixed", "meat_heavy"]
LevelType = Literal["low", "medium", "high"]
TravelFrequency = Literal["rare", "monthly", "frequent"]


class OnboardingInput(BaseModel):
    transport: TransportType
    food: FoodType
    energy: LevelType
    shopping: LevelType
    travel: TravelFrequency


class ProfileResponse(OnboardingInput):
    model_config = {"from_attributes": True}
