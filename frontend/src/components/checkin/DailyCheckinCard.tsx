"use client";

import { useState } from "react";
import { CheckCircle, Leaf, Loader2 } from "lucide-react";
import { Card, CardHeader, CardTitle } from "@/components/ui/Card";
import { Button } from "@/components/ui/Button";
import type { FootprintSnapshot } from "@/lib/types";

interface Props {
  /** The existing check-in for today, or null if not yet done. */
  todaysCheckin: FootprintSnapshot | null;
  onCheckin: () => Promise<void>;
}

export function DailyCheckinCard({ todaysCheckin, onCheckin }: Props) {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleClick = async () => {
    setLoading(true);
    setError(null);
    try {
      await onCheckin();
    } catch (err) {
      setError(err instanceof Error ? err.message : "Check-in failed. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  const alreadyDone = todaysCheckin !== null;

  return (
    <Card
      aria-label={alreadyDone ? "Today's check-in complete" : "Daily check-in"}
    >
      <CardHeader>
        <CardTitle>Daily Check-In</CardTitle>
        {alreadyDone && (
          <CheckCircle className="h-5 w-5 text-signal" aria-hidden="true" />
        )}
      </CardHeader>

      {alreadyDone ? (
        <div className="flex flex-col gap-2">
          <p className="text-sm text-mist-dim">
            You&apos;ve already logged today&apos;s footprint — great job!
          </p>
          <dl className="mt-2 grid grid-cols-2 gap-x-4 gap-y-1 text-sm">
            <dt className="text-mist-dim">Carbon score</dt>
            <dd className="font-semibold text-signal" aria-label={`Carbon score: ${todaysCheckin.carbon_score}`}>
              {todaysCheckin.carbon_score}
            </dd>
            <dt className="text-mist-dim">Total this month</dt>
            <dd className="font-semibold text-mist" aria-label={`${todaysCheckin.total_kg_co2_month} kg CO2`}>
              {todaysCheckin.total_kg_co2_month} kg CO2
            </dd>
          </dl>
        </div>
      ) : (
        <div className="flex flex-col gap-4">
          <p className="text-sm text-mist-dim">
            Log today&apos;s footprint to keep your trend chart up to date. It only takes a second.
          </p>

          {error && (
            <p role="alert" className="text-xs text-ember">
              {error}
            </p>
          )}

          <Button
            onClick={handleClick}
            disabled={loading}
            aria-label="Log today's footprint check-in"
          >
            {loading ? (
              <>
                <Loader2 className="h-4 w-4 animate-spin" aria-hidden="true" />
                <span>Checking in…</span>
              </>
            ) : (
              <>
                <Leaf className="h-4 w-4" aria-hidden="true" />
                <span>Check In Now</span>
              </>
            )}
          </Button>
        </div>
      )}
    </Card>
  );
}
