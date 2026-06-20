"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { RequireAuth } from "@/components/auth/RequireAuth";
import { OptionGrid } from "@/components/onboarding/OptionGrid";
import { Button } from "@/components/ui/Button";
import { Card } from "@/components/ui/Card";
import { useAuth } from "@/lib/auth-context";
import { api, ApiError } from "@/lib/api";
import type { OnboardingInput } from "@/lib/types";

type FieldKey = keyof OnboardingInput;

interface Step {
  key: FieldKey;
  legend: string;
  options: { value: string; label: string; description?: string }[];
}

const STEPS: Step[] = [
  {
    key: "transport",
    legend: "How do you usually get around?",
    options: [
      { value: "car", label: "Car", description: "Mostly drive, solo" },
      { value: "bike", label: "Bike", description: "Pedal power" },
      { value: "bus", label: "Bus", description: "Public bus routes" },
      { value: "train", label: "Train", description: "Rail or metro" },
      { value: "walking", label: "Walking", description: "On foot, mostly" },
    ],
  },
  {
    key: "food",
    legend: "What does your diet look like?",
    options: [
      { value: "vegetarian", label: "Vegetarian", description: "Little to no meat" },
      { value: "mixed", label: "Mixed", description: "A balance of both" },
      { value: "meat_heavy", label: "Meat-heavy", description: "Meat most meals" },
    ],
  },
  {
    key: "energy",
    legend: "How would you describe your home energy use?",
    options: [
      { value: "low", label: "Low", description: "Efficient, mindful usage" },
      { value: "medium", label: "Medium", description: "Fairly typical usage" },
      { value: "high", label: "High", description: "Heavy heating/cooling or appliance use" },
    ],
  },
  {
    key: "shopping",
    legend: "How often do you shop for new goods?",
    options: [
      { value: "low", label: "Low", description: "Buy only what's needed" },
      { value: "medium", label: "Medium", description: "Regular, moderate shopping" },
      { value: "high", label: "High", description: "Frequent new purchases" },
    ],
  },
  {
    key: "travel",
    legend: "How often do you take long-distance trips or flights?",
    options: [
      { value: "rare", label: "Rare", description: "Once a year or less" },
      { value: "monthly", label: "Monthly", description: "Roughly once a month" },
      { value: "frequent", label: "Frequent", description: "Multiple times a month" },
    ],
  },
];

export default function OnboardingPage() {
  const router = useRouter();
  const { token, refreshUser } = useAuth();
  const [stepIndex, setStepIndex] = useState(0);
  const [answers, setAnswers] = useState<Partial<OnboardingInput>>({});
  const [error, setError] = useState<string | null>(null);
  const [isSubmitting, setIsSubmitting] = useState(false);

  const step = STEPS[stepIndex];
  const currentValue = (answers[step.key] as string | undefined) ?? null;
  const isLastStep = stepIndex === STEPS.length - 1;

  async function handleNext() {
    if (!currentValue) return;
    if (!isLastStep) {
      setStepIndex((i) => i + 1);
      return;
    }
    if (!token) return;
    setError(null);
    setIsSubmitting(true);
    try {
      await api.submitOnboarding(token, answers as OnboardingInput);
      await refreshUser();
      router.push("/dashboard");
    } catch (err) {
      setError(err instanceof ApiError ? err.message : "Couldn't save your profile. Please try again.");
    } finally {
      setIsSubmitting(false);
    }
  }

  return (
    <RequireAuth requireOnboarding={false}>
      <main id="main-content" className="flex min-h-screen items-center justify-center px-4 py-10">
        <div className="w-full max-w-xl">
          <ol className="mb-6 flex items-center justify-center gap-2" aria-label="Onboarding progress">
            {STEPS.map((s, i) => (
              <li key={s.key}>
                <span
                  aria-current={i === stepIndex ? "step" : undefined}
                  className={`block h-1.5 w-10 rounded-full ${
                    i <= stepIndex ? "bg-signal" : "bg-white/10"
                  }`}
                >
                  <span className="sr-only">
                    Step {i + 1} of {STEPS.length}
                    {i < stepIndex ? " (completed)" : i === stepIndex ? " (current)" : ""}
                  </span>
                </span>
              </li>
            ))}
          </ol>

          <Card>
            <p className="mb-1 text-xs font-semibold uppercase tracking-wide text-mist-dim">
              Step {stepIndex + 1} of {STEPS.length}
            </p>
            <OptionGrid
              name={step.key}
              legend={step.legend}
              options={step.options}
              value={currentValue}
              onChange={(value) => setAnswers((prev) => ({ ...prev, [step.key]: value }))}
            />

            {error && (
              <p role="alert" className="mt-4 text-sm font-medium text-ember">
                {error}
              </p>
            )}

            <div className="mt-6 flex items-center justify-between">
              <Button
                type="button"
                variant="ghost"
                onClick={() => setStepIndex((i) => Math.max(0, i - 1))}
                disabled={stepIndex === 0}
              >
                Back
              </Button>
              <Button type="button" onClick={handleNext} disabled={!currentValue} loading={isSubmitting}>
                {isLastStep ? "Calculate my footprint" : "Next"}
              </Button>
            </div>
          </Card>
        </div>
      </main>
    </RequireAuth>
  );
}
