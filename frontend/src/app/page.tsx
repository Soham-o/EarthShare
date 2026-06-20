import Link from "next/link";
import { ArrowRight, Leaf, Sparkles, Store, TrendingUp } from "lucide-react";
import { Card } from "@/components/ui/Card";

const VALUE_PROPS = [
  {
    icon: TrendingUp,
    title: "Understand your footprint",
    body: "A two-minute onboarding turns your transport, food, energy, shopping, and travel habits into one clear carbon score.",
  },
  {
    icon: Sparkles,
    title: "Personalized AI insights",
    body: "Know exactly which habit moves the needle most, and what to do about it this week.",
  },
  {
    icon: Store,
    title: "Real, simple actions",
    body: "An action marketplace of concrete steps — each one shows exactly how much carbon it saves.",
  },
];

export default function LandingPage() {
  return (
    <div className="min-h-screen">
      <header className="mx-auto flex max-w-6xl items-center justify-between px-4 py-6 sm:px-6">
        <div className="flex items-center gap-2 font-display text-lg font-semibold">
          <Leaf className="h-5 w-5 text-signal" aria-hidden="true" />
          EarthShare
        </div>
        <nav aria-label="Account" className="flex items-center gap-3">
          <Link href="/login" className="text-sm font-medium text-mist-dim hover:text-mist">
            Log in
          </Link>
          <Link
            href="/register"
            className="rounded-xl bg-signal px-4 py-2 text-sm font-semibold text-obsidian hover:bg-signal/90"
          >
            Get started
          </Link>
        </nav>
      </header>

      <main id="main-content">
        <section className="mx-auto max-w-4xl px-4 pt-16 pb-20 text-center sm:px-6">
          <span className="mb-5 inline-flex items-center gap-2 rounded-full border border-ledger/30 bg-ledger-dim/30 px-4 py-1.5 text-xs font-semibold uppercase tracking-wide text-ledger">
            Carbon Footprint Awareness Platform
          </span>
          <h1 className="font-display text-4xl font-bold leading-tight text-mist sm:text-5xl">
            Own a share of the planet.
          </h1>
          <p className="mx-auto mt-5 max-w-2xl text-balance text-lg text-mist-dim">
            Carbon feels invisible — until it&apos;s yours. EarthShare turns your daily choices into a
            personal stake: a carbon score, a growing dividend, and a clear path to reducing what you emit.
          </p>
          <div className="mt-8 flex items-center justify-center gap-3">
            <Link
              href="/register"
              className="flex items-center gap-2 rounded-xl bg-signal px-6 py-3 font-semibold text-obsidian hover:bg-signal/90"
            >
              Calculate my footprint
              <ArrowRight className="h-4 w-4" aria-hidden="true" />
            </Link>
            <Link
              href="/login"
              className="rounded-xl border border-glass-border-strong px-6 py-3 font-semibold text-mist hover:bg-white/5"
            >
              I already have an account
            </Link>
          </div>
        </section>

        <section className="mx-auto max-w-6xl px-4 pb-24 sm:px-6">
          <div className="grid gap-5 sm:grid-cols-3">
            {VALUE_PROPS.map(({ icon: Icon, title, body }) => (
              <Card key={title}>
                <Icon className="h-6 w-6 text-signal" aria-hidden="true" />
                <h2 className="mt-4 font-display text-lg font-semibold text-mist">{title}</h2>
                <p className="mt-2 text-sm leading-relaxed text-mist-dim">{body}</p>
              </Card>
            ))}
          </div>
        </section>
      </main>
    </div>
  );
}
