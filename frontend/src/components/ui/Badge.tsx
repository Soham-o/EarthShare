import { HTMLAttributes } from "react";
import clsx from "clsx";

type Tone = "signal" | "glacier" | "ledger" | "ember" | "neutral";

const toneClasses: Record<Tone, string> = {
  signal: "bg-signal-dim text-signal",
  glacier: "bg-glacier-dim text-glacier",
  ledger: "bg-ledger-dim text-ledger",
  ember: "bg-ember-dim text-ember",
  neutral: "bg-white/5 text-mist-dim",
};

export function Badge({
  tone = "neutral",
  className,
  children,
  ...props
}: HTMLAttributes<HTMLSpanElement> & { tone?: Tone }) {
  return (
    <span
      className={clsx("inline-flex items-center rounded-full px-3 py-1 text-xs font-semibold", toneClasses[tone], className)}
      {...props}
    >
      {children}
    </span>
  );
}

export function Spinner({ label = "Loading" }: { label?: string }) {
  return (
    <div role="status" className="flex items-center gap-3 text-mist-dim">
      <span className="h-5 w-5 animate-spin rounded-full border-2 border-current border-t-transparent" aria-hidden="true" />
      <span>{label}</span>
    </div>
  );
}
