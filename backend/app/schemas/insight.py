from pydantic import BaseModel


class InsightsResponse(BaseModel):
    headline: str
    why_high: str
    biggest_opportunity: str
    weekly_action_plan: list[str]
    recommendations: list[str]
    future_self_message: str
    source: str  # "gemini" | "rule_based" — transparent about how the insight was produced


class ActionCardResponse(BaseModel):
    id: str
    title: str
    description: str
    category: str
    kg_co2_saved_month: float
    difficulty: str
    impact_score: int
    completed: bool


class ActionCompletionRequest(BaseModel):
    action_id: str


class BadgeResponse(BaseModel):
    id: str
    title: str
    description: str
    earned: bool


class ProgressResponse(BaseModel):
    weekly_trend: list[dict]
    badges: list[BadgeResponse]
    total_actions_completed: int
    total_kg_co2_saved: float
