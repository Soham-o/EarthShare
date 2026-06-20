import { describe, expect, it, vi } from "vitest";
import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { OptionGrid } from "@/components/onboarding/OptionGrid";

const OPTIONS = [
  { value: "car", label: "Car", description: "Mostly drive, solo" },
  { value: "bike", label: "Bike", description: "Pedal power" },
];

describe("OptionGrid", () => {
  it("renders as an accessible fieldset of radio options", () => {
    render(
      <OptionGrid name="transport" legend="How do you get around?" options={OPTIONS} value={null} onChange={() => {}} />
    );

    expect(screen.getByRole("group", { name: /how do you get around/i })).toBeInTheDocument();
    expect(screen.getAllByRole("radio")).toHaveLength(2);
  });

  it("marks the selected option as checked", () => {
    render(
      <OptionGrid name="transport" legend="How do you get around?" options={OPTIONS} value="bike" onChange={() => {}} />
    );

    expect(screen.getByRole("radio", { name: /bike/i })).toBeChecked();
    expect(screen.getByRole("radio", { name: /car/i })).not.toBeChecked();
  });

  it("is operable with the keyboard alone (tab + space)", async () => {
    const user = userEvent.setup();
    const handleChange = vi.fn();
    render(
      <OptionGrid name="transport" legend="How do you get around?" options={OPTIONS} value={null} onChange={handleChange} />
    );

    await user.tab(); // focus the first radio
    await user.keyboard(" "); // select it

    expect(handleChange).toHaveBeenCalledWith("car");
  });

  it("calls onChange with the clicked option's value", async () => {
    const user = userEvent.setup();
    const handleChange = vi.fn();
    render(
      <OptionGrid name="transport" legend="How do you get around?" options={OPTIONS} value={null} onChange={handleChange} />
    );

    await user.click(screen.getByText("Bike"));
    expect(handleChange).toHaveBeenCalledWith("bike");
  });
});
