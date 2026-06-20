"use client";

import { useEffect } from "react";
import { useRouter } from "next/navigation";
import { useAuth } from "@/lib/auth-context";
import { Spinner } from "@/components/ui/Badge";

export function RequireAuth({
  children,
  requireOnboarding = true,
}: {
  children: React.ReactNode;
  /** Set false only on the onboarding page itself, to avoid a redirect loop. */
  requireOnboarding?: boolean;
}) {
  const { token, user, isLoading } = useAuth();
  const router = useRouter();

  useEffect(() => {
    if (isLoading) return;
    if (!token) {
      router.replace("/login");
      return;
    }
    if (requireOnboarding && user && !user.has_completed_onboarding) {
      router.replace("/onboarding");
    }
  }, [isLoading, token, user, requireOnboarding, router]);

  if (isLoading || !token || (requireOnboarding && user && !user.has_completed_onboarding)) {
    return (
      <div className="flex min-h-screen items-center justify-center">
        <Spinner label="Loading your EarthShare account…" />
      </div>
    );
  }

  return <>{children}</>;
}
