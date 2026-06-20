import { describe, expect, it } from "vitest";
import { render, screen } from "@testing-library/react";
import { Field } from "@/components/ui/Field";

describe("Field", () => {
  it("associates the visible label with the input", () => {
    render(<Field label="Email" />);
    expect(screen.getByLabelText("Email")).toBeInTheDocument();
  });

  it("exposes an error message to assistive tech via aria-describedby and role=alert", () => {
    render(<Field label="Password" error="Password must be at least 8 characters" />);
    const input = screen.getByLabelText("Password");
    const alert = screen.getByRole("alert");

    expect(alert).toHaveTextContent("Password must be at least 8 characters");
    expect(input).toHaveAttribute("aria-invalid", "true");
    expect(input.getAttribute("aria-describedby")).toContain(alert.id);
  });

  it("exposes a hint via aria-describedby when there is no error", () => {
    render(<Field label="Password" hint="At least 8 characters" />);
    const input = screen.getByLabelText("Password");
    expect(input.getAttribute("aria-describedby")).toBeTruthy();
    expect(screen.queryByRole("alert")).not.toBeInTheDocument();
  });
});
