"use client";

import { useCallback, useEffect, useState } from "react";
import { useAuth } from "@/lib/auth-context";
import { ApiError } from "@/lib/api";

export function useAuthedFetch<T>(fetcher: (token: string) => Promise<T>) {
  const { token } = useAuth();
  const [data, setData] = useState<T | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  const load = useCallback(() => {
    if (!token) return;
    setIsLoading(true);
    setError(null);
    fetcher(token)
      .then(setData)
      .catch((err) => setError(err instanceof ApiError ? err.message : "Something went wrong."))
      .finally(() => setIsLoading(false));
    // fetcher is expected to be referentially stable (defined at module scope
    // or wrapped by the caller) — re-running on every render would be wasteful.
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [token]);

  useEffect(() => {
    load();
  }, [load]);

  // `reload` and `refetch` are identical — `reload` is the original name,
  // `refetch` is the alias used by dashboard for symmetry with React Query style.
  return { data, error, isLoading, reload: load, refetch: load };
}
