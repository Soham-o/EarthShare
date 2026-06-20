"use client";

import { useCallback } from "react";
import { Leaf, ListChecks } from "lucide-react";
import { RequireAuth } from "@/components/auth/RequireAuth";
import { AppShell } from "@/components/layout/AppShell";
import { Card, CardHeader, CardTitle } from "@/components/ui/Card";
import { Spinner } from "@/components/ui/Badge";
import { StatCard } from "@/components/dashboard/StatCard";
import { WeeklyTrendChart } from "@/components/progress/WeeklyTrendChart";
import { BadgeCard } from "@/components/progress/BadgeCard";
import { useAuthedFetch } from "@/lib/hooks";
import { api } from "@/lib/api";

export default function ProgressPage() {
  const fetcher = useCallback((token: string) => api.getProgress(token), []);
  const { data, error, isLoading } = useAuthedFetch(fetcher);

  return (
    <RequireAuth>
      <AppShell>
        <h1 className="font-display text-2xl font-bold text-mist">Your Progress</h1>
        <p className="mt-1 text-mist-dim">Every completed action, tracked and celebrated.</p>

        {isLoading && (
          <div className="mt-10">
            <Spinner label="Loading your progress…" />
          </div>
        )}

        {error && (
          <p role="alert" className="mt-6 text-ember">
            {error}
          </p>
        )}

        {data && (
          <div className="mt-8 grid gap-6 lg:grid-cols-3">
            <div className="grid gap-4 sm:grid-cols-2 lg:col-span-3">
              <StatCard
                icon={ListChecks}
                label="Actions completed"
                value={String(data.total_actions_completed)}
                tone="signal"
              />
              <StatCard
                icon={Leaf}
                label="Total CO2 saved"
                value={`${data.total_kg_co2_saved} kg`}
                sub="From completed marketplace actions"
                tone="ledger"
              />
            </div>

            <Card className="lg:col-span-2">
              <CardHeader>
                <CardTitle>Weekly trend</CardTitle>
              </CardHeader>
              {data.weekly_trend.length > 0 ? (
                <WeeklyTrendChart points={data.weekly_trend} />
              ) : (
                <p className="text-sm text-mist-dim">Complete onboarding to start building your trend.</p>
              )}
            </Card>

            <Card className="lg:col-span-1">
              <CardHeader>
                <CardTitle>Achievement badges</CardTitle>
              </CardHeader>
              <div className="flex flex-col gap-3">
                {data.badges.map((badge) => (
                  <BadgeCard key={badge.id} badge={badge} />
                ))}
              </div>
            </Card>
          </div>
        )}
      </AppShell>
    </RequireAuth>
  );
}
