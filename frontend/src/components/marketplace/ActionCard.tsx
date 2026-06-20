"use client";

import { CheckCircle2 } from "lucide-react";
import { Card } from "@/components/ui/Card";
import { Badge } from "@/components/ui/Badge";
import { Button } from "@/components/ui/Button";
import { CATEGORY_META } from "@/lib/category-meta";
import type { ActionCardResponse } from "@/lib/types";

const DIFFICULTY_TONE = { easy: "signal", medium: "ledger", hard: "ember" } as const;

export function ActionCard({
  action,
  onComplete,
  isCompleting,
}: {
  action: ActionCardResponse;
  onComplete: (id: string) => void;
  isCompleting: boolean;
}) {
  const meta = CATEGORY_META[action.category];
  const Icon = meta?.icon;

  return (
    <Card className="flex flex-col">
      <div className="flex items-start justify-between gap-2">
        <div className="flex items-center gap-2">
          {Icon && <Icon className="h-4 w-4 text-mist-dim" aria-hidden="true" />}
          <span className="text-xs font-medium uppercase tracking-wide text-mist-dim">{meta?.label ?? action.category}</span>
        </div>
        <Badge tone={DIFFICULTY_TONE[action.difficulty]}>{action.difficulty}</Badge>
      </div>

      <h3 className="mt-3 font-display text-base font-semibold text-mist">{action.title}</h3>
      <p className="mt-1.5 flex-1 text-sm text-mist-dim">{action.description}</p>

      <dl className="mt-4 flex items-center justify-between text-sm">
        <div>
          <dt className="text-mist-dim">Carbon saved</dt>
          <dd className="font-mono-tabular font-semibold text-signal">{action.kg_co2_saved_month} kg/mo</dd>
        </div>
        <div className="text-right">
          <dt className="text-mist-dim">Impact score</dt>
          <dd className="font-mono-tabular font-semibold text-mist">{action.impact_score}/100</dd>
        </div>
      </dl>

      <Button
        type="button"
        variant={action.completed ? "ghost" : "primary"}
        className="mt-4 w-full"
        disabled={action.completed}
        loading={isCompleting}
        onClick={() => onComplete(action.id)}
      >
        {action.completed ? (
          <>
            <CheckCircle2 className="h-4 w-4" aria-hidden="true" /> Completed
          </>
        ) : (
          "Mark as done"
        )}
      </Button>
    </Card>
  );
}
