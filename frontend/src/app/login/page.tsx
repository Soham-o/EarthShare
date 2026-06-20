"use client";

import { useState, FormEvent } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { Leaf } from "lucide-react";
import { useAuth } from "@/lib/auth-context";
import { ApiError } from "@/lib/api";
import { Card } from "@/components/ui/Card";
import { Field } from "@/components/ui/Field";
import { Button } from "@/components/ui/Button";

export default function LoginPage() {
  const router = useRouter();
  const { login } = useAuth();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState<string | null>(null);
  const [isSubmitting, setIsSubmitting] = useState(false);

  async function handleSubmit(e: FormEvent) {
    e.preventDefault();
    setError(null);
    setIsSubmitting(true);
    try {
      await login(email, password);
      router.push("/dashboard");
    } catch (err) {
      setError(err instanceof ApiError ? err.message : "Something went wrong. Please try again.");
    } finally {
      setIsSubmitting(false);
    }
  }

  return (
    <main id="main-content" className="flex min-h-screen items-center justify-center px-4">
      <div className="w-full max-w-sm">
        <div className="mb-6 flex items-center justify-center gap-2 font-display text-lg font-semibold text-mist">
          <Leaf className="h-5 w-5 text-signal" aria-hidden="true" />
          EarthShare
        </div>
        <Card>
          <h1 className="font-display text-xl font-semibold text-mist">Welcome back</h1>
          <p className="mt-1 text-sm text-mist-dim">Log in to see your latest carbon score.</p>

          <form onSubmit={handleSubmit} className="mt-6 flex flex-col gap-4" noValidate>
            <Field
              label="Email"
              type="email"
              autoComplete="email"
              required
              value={email}
              onChange={(e) => setEmail(e.target.value)}
            />
            <Field
              label="Password"
              type="password"
              autoComplete="current-password"
              required
              value={password}
              onChange={(e) => setPassword(e.target.value)}
            />
            {error && (
              <p role="alert" className="text-sm font-medium text-ember">
                {error}
              </p>
            )}
            <Button type="submit" loading={isSubmitting} className="mt-2 w-full">
              Log in
            </Button>
          </form>

          <p className="mt-5 text-center text-sm text-mist-dim">
            New here?{" "}
            <Link href="/register" className="font-semibold text-signal hover:underline">
              Create an account
            </Link>
          </p>
        </Card>
      </div>
    </main>
  );
}
