import { Award, Lock } from "lucide-react";
import { Card } from "@/components/ui/Card";
import type { BadgeResponse } from "@/lib/types";

export function BadgeCard({ badge }: { badge: BadgeResponse }) {
  return (
    <Card className={`flex items-center gap-3 ${badge.earned ? "border-ledger/40 bg-ledger-dim/20" : "opacity-60"}`}>
      {badge.earned ? (
        <Award className="h-6 w-6 shrink-0 text-ledger" aria-hidden="true" />
      ) : (
        <Lock className="h-6 w-6 shrink-0 text-mist-faint" aria-hidden="true" />
      )}
      <div>
        <p className="font-display text-sm font-semibold text-mist">{badge.title}</p>
        <p className="text-xs text-mist-dim">{badge.description}</p>
        <span className="sr-only">{badge.earned ? "Earned" : "Not yet earned"}</span>
      </div>
    </Card>
  );
}
