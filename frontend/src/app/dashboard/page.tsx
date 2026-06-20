"use client";

import { useCallback } from "react";
import { Coins, Gauge, Leaf, TrendingDown, TrendingUp } from "lucide-react";
import { RequireAuth } from "@/components/auth/RequireAuth";
import { AppShell } from "@/components/layout/AppShell";
import { Card, CardHeader, CardTitle } from "@/components/ui/Card";
import { Badge, Spinner } from "@/components/ui/Badge";
import { EquityRing } from "@/components/dashboard/EquityRing";
import { StatCard } from "@/components/dashboard/StatCard";
import { TrendChart } from "@/components/dashboard/TrendChart";
import { EmissionBreakdownChart } from "@/components/dashboard/EmissionBreakdownChart";
import { DailyCheckinCard } from "@/components/checkin/DailyCheckinCard";
import { CATEGORY_META } from "@/lib/category-meta";
import { useAuthedFetch } from "@/lib/hooks";
import { useAuth } from "@/lib/auth-context";
import { api } from "@/lib/api";
import type { FootprintSnapshot } from "@/lib/types";

export default function DashboardPage() {
  const { token } = useAuth();

  const dashFetcher = useCallback((t: string) => api.getDashboard(t), []);
  const { data, error, isLoading, refetch: refetchDashboard } = useAuthedFetch(dashFetcher);

  const checkinFetcher = useCallback((t: string) => api.getTodaysCheckin(t), []);
  const { data: todaysCheckin, refetch: refetchCheckin } = useAuthedFetch<FootprintSnapshot | undefined>(checkinFetcher);

  const handleCheckin = useCallback(async () => {
    if (!token) return;
    await api.dailyCheckin(token);
    // Refresh both the check-in card status and the dashboard trend chart
    refetchCheckin();
    refetchDashboard();
  }, [token, refetchCheckin, refetchDashboard]);

  return (
    <RequireAuth>
      <AppShell>
        <h1 className="font-display text-2xl font-bold text-mist">Your EarthShare Dashboard</h1>
        <p className="mt-1 text-mist-dim">A live snapshot of your footprint, and what it&apos;s worth.</p>

        {isLoading && (
          <div className="mt-10">
            <Spinner label="Calculating your footprint…" />
          </div>
        )}

        {error && (
          <p role="alert" className="mt-6 text-ember">
            {error}
          </p>
        )}

        {data && (
          <div className="mt-8 grid gap-6 lg:grid-cols-3">
            {/* Daily Check-In — spans full width, keeps trend chart current */}
            <div className="lg:col-span-3">
              <DailyCheckinCard
                todaysCheckin={todaysCheckin ?? null}
                onCheckin={handleCheckin}
              />
            </div>

            <Card className="flex flex-col items-center justify-center lg:col-span-1">
              <EquityRing score={data.carbon_score} shares={data.dividend_shares} />
              <p className="mt-4 text-center text-sm text-mist-dim">
                {data.total_kg_co2_month} kg CO2 this month — vs a typical {data.national_average_kg_co2_month} kg.
              </p>
            </Card>

            <div className="grid gap-4 sm:grid-cols-2 lg:col-span-2">
              <StatCard
                icon={Coins}
                label="EarthShare Dividend"
                value={data.earthshare_dividend.toLocaleString()}
                sub={`${data.dividend_shares} shares held`}
                tone="ledger"
              />
              <StatCard
                icon={Gauge}
                label="Reduction potential"
                value={`${data.reduction_potential_kg_co2_month} kg`}
                sub="Available this month from the action marketplace"
                tone="signal"
              />
              <StatCard
                icon={TrendingUp}
                label="Projected this year"
                value={`${data.future_projection_kg_co2_year} kg`}
                sub="If nothing changes"
                tone="mist"
              />
              <StatCard
                icon={TrendingDown}
                label="Improved projection"
                value={`${data.improved_projection_kg_co2_year} kg`}
                sub="If you complete your top 2 recommended actions"
                tone="glacier"
              />
            </div>

            <Card className="lg:col-span-2">
              <CardHeader>
                <CardTitle>Monthly trend</CardTitle>
              </CardHeader>
              <TrendChart trend={data.monthly_trend} />
            </Card>

            <Card className="lg:col-span-1">
              <CardHeader>
                <CardTitle>Top emission sources</CardTitle>
              </CardHeader>
              <ul className="flex flex-col gap-3">
                {data.top_emission_sources.map((source) => {
                  const meta = CATEGORY_META[source.category];
                  const Icon = meta?.icon;
                  return (
                    <li key={source.category} className="flex items-center justify-between gap-2">
                      <span className="flex items-center gap-2 text-sm text-mist">
                        {Icon && <Icon className="h-4 w-4 text-mist-dim" aria-hidden="true" />}
                        {meta?.label ?? source.category}
                      </span>
                      <Badge tone="ember">{source.kg_co2_month} kg</Badge>
                    </li>
                  );
                })}
              </ul>
            </Card>

            <Card className="lg:col-span-3">
              <CardHeader>
                <CardTitle>Footprint breakdown</CardTitle>
              </CardHeader>
              <EmissionBreakdownChart breakdown={data.monthly_trend[data.monthly_trend.length - 1]?.breakdown ?? []} />
            </Card>

            <Card className="flex items-center gap-3 lg:col-span-3">
              <Leaf className="h-5 w-5 shrink-0 text-signal" aria-hidden="true" />
              <p className="text-sm text-mist-dim">
                Want a deeper look at why your score is what it is?{" "}
                <a href="/insights" className="font-semibold text-signal hover:underline">
                  See your personalized insights
                </a>
                .
              </p>
            </Card>
          </div>
        )}
      </AppShell>
    </RequireAuth>
  );
}
