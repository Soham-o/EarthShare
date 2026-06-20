"use client";

interface Option {
  value: string;
  label: string;
  description?: string;
}

export function OptionGrid({
  name,
  legend,
  options,
  value,
  onChange,
}: {
  name: string;
  legend: string;
  options: Option[];
  value: string | null;
  onChange: (value: string) => void;
}) {
  return (
    <fieldset>
      <legend className="font-display text-xl font-semibold text-mist">{legend}</legend>
      <div className="mt-4 grid gap-3 sm:grid-cols-2">
        {options.map((opt) => {
          const id = `${name}-${opt.value}`;
          const checked = value === opt.value;
          return (
            <div key={opt.value}>
              <input
                type="radio"
                id={id}
                name={name}
                value={opt.value}
                checked={checked}
                onChange={() => onChange(opt.value)}
                className="peer sr-only"
              />
              <label
                htmlFor={id}
                className="block cursor-pointer rounded-xl border border-glass-border-strong bg-pine/50 p-4 transition-colors peer-checked:border-signal peer-checked:bg-signal/10 peer-focus-visible:outline peer-focus-visible:outline-2 peer-focus-visible:outline-signal hover:border-mist-faint"
              >
                <span className="font-medium text-mist">{opt.label}</span>
                {opt.description && <span className="mt-0.5 block text-sm text-mist-dim">{opt.description}</span>}
              </label>
            </div>
          );
        })}
      </div>
    </fieldset>
  );
}
