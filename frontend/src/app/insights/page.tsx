"use client";

import { useCallback } from "react";
import { CheckCircle2, MessageCircleHeart, Sparkles, Target } from "lucide-react";
import { RequireAuth } from "@/components/auth/RequireAuth";
import { AppShell } from "@/components/layout/AppShell";
import { Card, CardHeader, CardTitle } from "@/components/ui/Card";
import { Badge, Spinner } from "@/components/ui/Badge";
import { useAuthedFetch } from "@/lib/hooks";
import { api } from "@/lib/api";

export default function InsightsPage() {
  const fetcher = useCallback((token: string) => api.getInsights(token), []);
  const { data, error, isLoading } = useAuthedFetch(fetcher);

  return (
    <RequireAuth>
      <AppShell>
        <div className="flex items-center justify-between gap-3">
          <div>
            <h1 className="font-display text-2xl font-bold text-mist">Personalized Insights</h1>
            <p className="mt-1 text-mist-dim">Why your footprint looks the way it does, and what to do next.</p>
          </div>
          {data && (
            <Badge tone={data.source === "gemini" ? "glacier" : "neutral"}>
              {data.source === "gemini" ? "Gemini-enhanced" : "Rule-based"}
            </Badge>
          )}
        </div>

        {isLoading && (
          <div className="mt-10">
            <Spinner label="Generating your insights…" />
          </div>
        )}

        {error && (
          <p role="alert" className="mt-6 text-ember">
            {error}
          </p>
        )}

        {data && (
          <div className="mt-8 grid gap-6 lg:grid-cols-2">
            <Card className="lg:col-span-2">
              <div className="flex items-start gap-3">
                <Sparkles className="mt-0.5 h-5 w-5 shrink-0 text-signal" aria-hidden="true" />
                <p className="font-display text-lg leading-snug text-mist">{data.headline}</p>
              </div>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle>Why it&apos;s high</CardTitle>
              </CardHeader>
              <p className="text-sm leading-relaxed text-mist-dim">{data.why_high}</p>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle>Biggest opportunity</CardTitle>
              </CardHeader>
              <div className="flex items-start gap-2">
                <Target className="mt-0.5 h-4 w-4 shrink-0 text-glacier" aria-hidden="true" />
                <p className="text-sm leading-relaxed text-mist-dim">{data.biggest_opportunity}</p>
              </div>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle>This week&apos;s action plan</CardTitle>
              </CardHeader>
              <ul className="flex flex-col gap-2">
                {data.weekly_action_plan.map((item, i) => (
                  <li key={i} className="flex items-start gap-2 text-sm text-mist">
                    <CheckCircle2 className="mt-0.5 h-4 w-4 shrink-0 text-signal" aria-hidden="true" />
                    {item}
                  </li>
                ))}
              </ul>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle>Recommendations</CardTitle>
              </CardHeader>
              <ul className="flex flex-col gap-2">
                {data.recommendations.map((item, i) => (
                  <li key={i} className="text-sm leading-relaxed text-mist-dim">
                    • {item}
                  </li>
                ))}
              </ul>
            </Card>

            <Card className="flex items-start gap-3 border-ledger/30 bg-ledger-dim/20 lg:col-span-2">
              <MessageCircleHeart className="mt-0.5 h-5 w-5 shrink-0 text-ledger" aria-hidden="true" />
              <div>
                <CardTitle className="text-ledger">Your Future Self</CardTitle>
                <p className="mt-2 text-sm leading-relaxed text-mist">{data.future_self_message}</p>
              </div>
            </Card>
          </div>
        )}
      </AppShell>
    </RequireAuth>
  );
}
