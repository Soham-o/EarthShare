import { Bus, Car as CarIcon, Lightbulb, Plane, ShoppingBag, Utensils } from "lucide-react";

export const CATEGORY_META: Record<
  string,
  { label: string; icon: typeof CarIcon; color: string; barColor: string }
> = {
  transport: { label: "Transport", icon: CarIcon, color: "var(--color-glacier)", barColor: "#5ec8e0" },
  food: { label: "Food", icon: Utensils, color: "var(--color-signal)", barColor: "#4ade80" },
  energy: { label: "Home energy", icon: Lightbulb, color: "var(--color-ledger)", barColor: "#e8c468" },
  shopping: { label: "Shopping", icon: ShoppingBag, color: "var(--color-ember)", barColor: "#f2935a" },
  travel: { label: "Long-distance travel", icon: Plane, color: "#b794f4", barColor: "#b794f4" },
};

export const FALLBACK_ICON = Bus;
