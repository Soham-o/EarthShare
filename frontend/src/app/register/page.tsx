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

export default function RegisterPage() {
  const router = useRouter();
  const { register } = useAuth();
  const [fullName, setFullName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState<string | null>(null);
  const [isSubmitting, setIsSubmitting] = useState(false);

  async function handleSubmit(e: FormEvent) {
    e.preventDefault();
    setError(null);
    setIsSubmitting(true);
    try {
      await register(email, fullName, password);
      router.push("/onboarding");
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
          <h1 className="font-display text-xl font-semibold text-mist">Create your account</h1>
          <p className="mt-1 text-sm text-mist-dim">Takes under a minute. No credit card, obviously.</p>

          <form onSubmit={handleSubmit} className="mt-6 flex flex-col gap-4" noValidate>
            <Field
              label="Full name"
              autoComplete="name"
              required
              value={fullName}
              onChange={(e) => setFullName(e.target.value)}
            />
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
              autoComplete="new-password"
              required
              minLength={8}
              hint="At least 8 characters, with letters and numbers."
              value={password}
              onChange={(e) => setPassword(e.target.value)}
            />
            {error && (
              <p role="alert" className="text-sm font-medium text-ember">
                {error}
              </p>
            )}
            <Button type="submit" loading={isSubmitting} className="mt-2 w-full">
              Create account
            </Button>
          </form>

          <p className="mt-5 text-center text-sm text-mist-dim">
            Already have an account?{" "}
            <Link href="/login" className="font-semibold text-signal hover:underline">
              Log in
            </Link>
          </p>
        </Card>
      </div>
    </main>
  );
}
