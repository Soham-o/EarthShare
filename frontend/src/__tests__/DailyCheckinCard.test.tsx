import { describe, expect, it, vi } from "vitest";
import { render, screen, fireEvent, waitFor } from "@testing-library/react";
import { axe } from "vitest-axe";
import { DailyCheckinCard } from "@/components/checkin/DailyCheckinCard";

const mockCheckin: import("@/lib/types").FootprintSnapshot = {
  total_kg_co2_month: 400,
  carbon_score: 647,
  breakdown: [],
  created_at: new Date().toISOString(),
};

describe("DailyCheckinCard", () => {
  it("has no detectable a11y violations when not yet checked in", async () => {
    const { container } = render(
      <DailyCheckinCard todaysCheckin={null} onCheckin={vi.fn()} />
    );
    const results = await axe(container);
    expect(results).toHaveNoViolations();
  });

  it("has no detectable a11y violations when already checked in", async () => {
    const { container } = render(
      <DailyCheckinCard todaysCheckin={mockCheckin} onCheckin={vi.fn()} />
    );
    const results = await axe(container);
    expect(results).toHaveNoViolations();
  });

  it("shows check-in button when not yet checked in", () => {
    render(<DailyCheckinCard todaysCheckin={null} onCheckin={vi.fn()} />);
    // aria-label is "Log today's footprint check-in"
    expect(
      screen.getByRole("button", { name: /log today's footprint check-in/i })
    ).toBeInTheDocument();
  });

  it("shows success state when already checked in", () => {
    render(<DailyCheckinCard todaysCheckin={mockCheckin} onCheckin={vi.fn()} />);
    expect(screen.queryByRole("button")).not.toBeInTheDocument();
    expect(screen.getByText(/already logged/i)).toBeInTheDocument();
    expect(screen.getByText("647")).toBeInTheDocument();
  });

  it("calls onCheckin when button is clicked", async () => {
    const onCheckin = vi.fn().mockResolvedValue(undefined);
    render(<DailyCheckinCard todaysCheckin={null} onCheckin={onCheckin} />);
    fireEvent.click(
      screen.getByRole("button", { name: /log today's footprint check-in/i })
    );
    await waitFor(() => expect(onCheckin).toHaveBeenCalledOnce());
  });

  it("displays error message on checkin failure", async () => {
    const onCheckin = vi.fn().mockRejectedValue(new Error("Network error"));
    render(<DailyCheckinCard todaysCheckin={null} onCheckin={onCheckin} />);
    fireEvent.click(
      screen.getByRole("button", { name: /log today's footprint check-in/i })
    );
    await waitFor(() => expect(screen.getByRole("alert")).toBeInTheDocument());
    expect(screen.getByRole("alert")).toHaveTextContent("Network error");
  });
});
