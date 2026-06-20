export type TransportType = "car" | "bike" | "bus" | "train" | "walking";
export type FoodType = "vegetarian" | "mixed" | "meat_heavy";
export type LevelType = "low" | "medium" | "high";
export type TravelFrequency = "rare" | "monthly" | "frequent";

export interface OnboardingInput {
  transport: TransportType;
  food: FoodType;
  energy: LevelType;
  shopping: LevelType;
  travel: TravelFrequency;
}

export interface UserPublic {
  id: string;
  email: string;
  full_name: string;
  has_completed_onboarding: boolean;
}

export interface CategoryBreakdown {
  category: string;
  kg_co2_month: number;
  percent_of_total: number;
}

export interface FootprintSnapshot {
  total_kg_co2_month: number;
  carbon_score: number;
  breakdown: CategoryBreakdown[];
  created_at: string;
}

export interface EmissionSource {
  category: string;
  kg_co2_month: number;
  label: string;
}

export interface DashboardResponse {
  carbon_score: number;
  total_kg_co2_month: number;
  monthly_trend: FootprintSnapshot[];
  earthshare_dividend: number;
  dividend_shares: number;
  future_projection_kg_co2_year: number;
  improved_projection_kg_co2_year: number;
  top_emission_sources: EmissionSource[];
  reduction_potential_kg_co2_month: number;
  national_average_kg_co2_month: number;
}

export interface InsightsResponse {
  headline: string;
  why_high: string;
  biggest_opportunity: string;
  weekly_action_plan: string[];
  recommendations: string[];
  future_self_message: string;
  source: "gemini" | "rule_based";
}

export interface ActionCardResponse {
  id: string;
  title: string;
  description: string;
  category: string;
  kg_co2_saved_month: number;
  difficulty: "easy" | "medium" | "hard";
  impact_score: number;
  completed: boolean;
}

export interface BadgeResponse {
  id: string;
  title: string;
  description: string;
  earned: boolean;
}

export interface ProgressResponse {
  weekly_trend: { date: string; carbon_score: number; total_kg_co2_month: number }[];
  badges: BadgeResponse[];
  total_actions_completed: number;
  total_kg_co2_saved: number;
}
