from datetime import datetime

from pydantic import BaseModel


class CategoryBreakdown(BaseModel):
    category: str
    kg_co2_month: float
    percent_of_total: float


class EmissionSource(BaseModel):
    category: str
    kg_co2_month: float
    label: str  # accessible text label, doubles as the non-color chart legend


class FootprintSnapshot(BaseModel):
    total_kg_co2_month: float
    carbon_score: int
    breakdown: list[CategoryBreakdown]
    created_at: datetime


class DashboardResponse(BaseModel):
    carbon_score: int
    total_kg_co2_month: float
    monthly_trend: list[FootprintSnapshot]
    earthshare_dividend: float
    dividend_shares: int
    future_projection_kg_co2_year: float
    improved_projection_kg_co2_year: float
    top_emission_sources: list[EmissionSource]
    reduction_potential_kg_co2_month: float
    national_average_kg_co2_month: float
