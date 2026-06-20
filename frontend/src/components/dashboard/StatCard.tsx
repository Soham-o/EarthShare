import { LucideIcon } from "lucide-react";
import { Card } from "@/components/ui/Card";

export function StatCard({
  icon: Icon,
  label,
  value,
  sub,
  tone = "mist",
}: {
  icon: LucideIcon;
  label: string;
  value: string;
  sub?: string;
  tone?: "mist" | "signal" | "glacier" | "ledger";
}) {
  const toneColor =
    tone === "signal" ? "text-signal" : tone === "glacier" ? "text-glacier" : tone === "ledger" ? "text-ledger" : "text-mist";

  return (
    <Card className="p-5">
      <div className="flex items-center gap-2 text-mist-dim">
        <Icon className="h-4 w-4" aria-hidden="true" />
        <span className="text-sm">{label}</span>
      </div>
      <p className={`font-mono-tabular mt-2 text-2xl font-semibold ${toneColor}`}>{value}</p>
      {sub && <p className="mt-1 text-xs text-mist-dim">{sub}</p>}
    </Card>
  );
}
