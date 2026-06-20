import { describe, expect, it } from "vitest";
import { render, screen } from "@testing-library/react";
import { EquityRing } from "@/components/dashboard/EquityRing";

describe("EquityRing", () => {
  it("exposes score and share count to assistive tech via a single descriptive label", () => {
    render(<EquityRing score={742} shares={3} />);
    const ring = screen.getByRole("img", { name: /carbon score 742 out of 1000/i });
    expect(ring).toHaveAccessibleName(expect.stringContaining("3 EarthShare shares"));
  });

  it("uses singular phrasing for exactly one share", () => {
    render(<EquityRing score={500} shares={1} />);
    expect(screen.getByRole("img")).toHaveAccessibleName(expect.stringContaining("1 EarthShare share,"));
  });

  it("does not expose the decorative SVG/animation separately to screen readers", () => {
    const { container } = render(<EquityRing score={600} shares={2} />);
    // The SVG and the glow ring must be aria-hidden; only the wrapping role="img" should be announced.
    const svg = container.querySelector("svg");
    expect(svg).toHaveAttribute("aria-hidden", "true");
  });

  it("renders the certificate serial number padded to six digits", () => {
    render(<EquityRing score={500} shares={7} />);
    expect(screen.getByText(/SHARE Nº000007/)).toBeInTheDocument();
  });
});
