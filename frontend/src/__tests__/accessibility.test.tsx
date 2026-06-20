import { describe, expect, it } from "vitest";
import { render } from "@testing-library/react";
import { axe } from "vitest-axe";
import { OptionGrid } from "@/components/onboarding/OptionGrid";
import { Field } from "@/components/ui/Field";
import { Button } from "@/components/ui/Button";
import { Card, CardHeader, CardTitle } from "@/components/ui/Card";
import { Badge } from "@/components/ui/Badge";
import { EquityRing } from "@/components/dashboard/EquityRing";
import LandingPage from "@/app/page";

describe("accessibility (axe)", () => {
  it("landing page has no detectable a11y violations", async () => {
    const { container } = render(<LandingPage />);
    const results = await axe(container);
    expect(results).toHaveNoViolations();
  });

  it("onboarding OptionGrid has no detectable a11y violations", async () => {
    const { container } = render(
      <OptionGrid
        name="food"
        legend="What does your diet look like?"
        options={[
          { value: "vegetarian", label: "Vegetarian" },
          { value: "mixed", label: "Mixed" },
        ]}
        value="mixed"
        onChange={() => {}}
      />
    );
    const results = await axe(container);
    expect(results).toHaveNoViolations();
  });

  it("a labeled form field with an error message has no detectable a11y violations", async () => {
    const { container } = render(
      <form>
        <Field label="Email" type="email" error="Enter a valid email address" />
        <Button type="submit">Continue</Button>
      </form>
    );
    const results = await axe(container);
    expect(results).toHaveNoViolations();
  });

  it("a card composition with badges and the equity ring has no detectable a11y violations", async () => {
    const { container } = render(
      <Card>
        <CardHeader>
          <CardTitle>Dashboard summary</CardTitle>
          <Badge tone="signal">On track</Badge>
        </CardHeader>
        <EquityRing score={812} shares={4} />
      </Card>
    );
    const results = await axe(container);
    expect(results).toHaveNoViolations();
  });
});
