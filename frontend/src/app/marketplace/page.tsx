"use client";

import { useCallback, useState } from "react";
import { RequireAuth } from "@/components/auth/RequireAuth";
import { AppShell } from "@/components/layout/AppShell";
import { Spinner } from "@/components/ui/Badge";
import { ActionCard } from "@/components/marketplace/ActionCard";
import { useAuthedFetch } from "@/lib/hooks";
import { useAuth } from "@/lib/auth-context";
import { api, ApiError } from "@/lib/api";

export default function MarketplacePage() {
  const { token } = useAuth();
  const fetcher = useCallback((t: string) => api.getActions(t), []);
  const { data, error, isLoading, reload } = useAuthedFetch(fetcher);
  const [pendingId, setPendingId] = useState<string | null>(null);
  const [actionError, setActionError] = useState<string | null>(null);

  async function handleComplete(actionId: string) {
    if (!token) return;
    setPendingId(actionId);
    setActionError(null);
    try {
      await api.completeAction(token, actionId);
      reload();
    } catch (err) {
      setActionError(err instanceof ApiError ? err.message : "Couldn't complete that action.");
    } finally {
      setPendingId(null);
    }
  }

  return (
    <RequireAuth>
      <AppShell>
        <h1 className="font-display text-2xl font-bold text-mist">Action Marketplace</h1>
        <p className="mt-1 text-mist-dim">Small, concrete steps — each one shows exactly what it&apos;s worth.</p>

        {isLoading && (
          <div className="mt-10">
            <Spinner label="Loading actions…" />
          </div>
        )}

        {(error || actionError) && (
          <p role="alert" className="mt-6 text-ember">
            {error ?? actionError}
          </p>
        )}

        {data && (
          <div className="mt-8 grid gap-5 sm:grid-cols-2 lg:grid-cols-3">
            {data.map((action) => (
              <ActionCard
                key={action.id}
                action={action}
                onComplete={handleComplete}
                isCompleting={pendingId === action.id}
              />
            ))}
          </div>
        )}
      </AppShell>
    </RequireAuth>
  );
}
