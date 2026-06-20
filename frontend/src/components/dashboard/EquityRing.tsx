"use client";

const RADIUS = 84;
const STROKE = 14;
const CIRCUMFERENCE = 2 * Math.PI * RADIUS;

export function EquityRing({ score, shares }: { score: number; shares: number }) {
  const fraction = Math.max(0, Math.min(1, score / 1000));
  const dashOffset = CIRCUMFERENCE * (1 - fraction);
  const serial = String(shares).padStart(6, "0");

  return (
    <div
      role="img"
      aria-label={`Carbon score ${score} out of 1000. You hold ${shares} EarthShare ${shares === 1 ? "share" : "shares"}, certificate number ${serial}.`}
      className="relative flex h-52 w-52 items-center justify-center"
    >
      {/* 1. Added absolute inset-0 here so it ignores flex layout and centers */}
      <svg viewBox="0 0 200 200" className="absolute inset-0 h-full w-full -rotate-90" aria-hidden="true">
        <circle cx="100" cy="100" r={RADIUS} fill="none" stroke="rgba(255,255,255,0.08)" strokeWidth={STROKE} />
        <circle
          cx="100"
          cy="100"
          r={RADIUS}
          fill="none"
          stroke="var(--color-signal)"
          strokeWidth={STROKE}
          strokeLinecap="round"
          strokeDasharray={CIRCUMFERENCE}
          strokeDashoffset={dashOffset}
          style={{ transition: "stroke-dashoffset 700ms ease-out" }}
        />
      </svg>

      {/* Ambient glow ring */}
      <div
        aria-hidden="true"
        className="pointer-events-none absolute inset-3 rounded-full border border-signal/30"
        style={{ animation: "ring-glow 3.5s ease-in-out infinite" }}
      />

      {/* 2. Added relative z-10 here so the text stacks on top of the SVG background */}
      <div aria-hidden="true" className="relative z-10 flex flex-col items-center gap-1 text-center">
        <span className="font-mono-tabular text-4xl font-semibold text-mist">{score}</span>
        <span className="text-xs uppercase tracking-wide text-mist-dim">Carbon Score</span>
        <div className="mt-2 rounded-md border border-ledger/40 bg-ledger-dim/40 px-2.5 py-1">
          <span className="font-mono-tabular text-[10px] tracking-widest text-ledger">SHARE Nº{serial}</span>
        </div>
      </div>
    </div>
  );
}