"use client";

import { InputHTMLAttributes, useId } from "react";

interface FieldProps extends InputHTMLAttributes<HTMLInputElement> {
  label: string;
  error?: string;
  hint?: string;
}

export function Field({ label, error, hint, id, ...props }: FieldProps) {
  const autoId = useId();
  const inputId = id ?? autoId;
  const hintId = `${inputId}-hint`;
  const errorId = `${inputId}-error`;

  return (
    <div className="flex flex-col gap-1.5">
      <label htmlFor={inputId} className="text-sm font-medium text-mist">
        {label}
      </label>
      <input
        id={inputId}
        aria-describedby={[hint && hintId, error && errorId].filter(Boolean).join(" ") || undefined}
        aria-invalid={error ? true : undefined}
        className="rounded-xl border border-glass-border-strong bg-pine/60 px-4 py-2.5 text-mist placeholder:text-mist-faint focus:border-signal"
        {...props}
      />
      {hint && !error && (
        <span id={hintId} className="text-xs text-mist-dim">
          {hint}
        </span>
      )}
      {error && (
        <span id={errorId} role="alert" className="text-xs font-medium text-ember">
          {error}
        </span>
      )}
    </div>
  );
}
