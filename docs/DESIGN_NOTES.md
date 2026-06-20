# EarthShare — Design Notes

## Brief constraints (taken as fixed)
Dark mode, green/blue sustainability palette, glassmorphism, subtle animation,
premium/minimal. These came directly from the project brief and are followed
exactly rather than re-interpreted.

## Token system

**Color**
| Token | Hex | Role |
|---|---|---|
| Obsidian | `#0B1410` | page background |
| Pine | `#11231C` | glass card surface |
| Signal (green) | `#4ADE80` | growth / positive change |
| Glacier (blue) | `#5EC8E0` | future / projection |
| Ledger (gold) | `#E8C468` | ownership / dividend / shares |
| Ember (warm orange) | `#F2935A` | highest-emission flag |
| Mist | `#E7EFE9` | primary text on dark |

Ember was chosen instead of red specifically so the "high emission" signal
isn't a pure red/green pair, which is the single most common colorblind
failure mode. Every chart also carries a text label, never relies on hue
alone.

**Type**
- Display: Space Grotesk — geometric, a little technical, used for headings
  and big numbers. Reads "ledger / fintech-for-the-planet," not "eco poster."
- Body: Inter — neutral, highly legible at small sizes, does the actual
  reading work.
- Mono: JetBrains Mono — used only for numeric data (carbon score, kg CO2,
  dividend figures) so they read like ticking ledger entries rather than
  prose, and so changing digits don't reflow surrounding text.

**Signature element: the Equity Ring**
A circular badge on the dashboard that doubles as a stock/share certificate
and a progress ring: the carbon score is the arc fill, and at the center
sits a serial number ("SHARE №000142") styled like a certificate seal. It's
the one place the "own a share of the planet" tagline becomes a literal
object instead of a metaphor in copy. Everything else on the page — cards,
charts, nav — stays quiet so this one element carries the personality.

## Restraint choices
- No numbered-step markers anywhere onboarding isn't a literal fixed
  sequence with meaning to the order (it is, here — 5 steps — so the
  onboarding flow does use a 1-5 progress indicator; nowhere else does).
- One signature animation (the ring's slow ambient glow), not scattered
  micro-animations. Reduced-motion is respected globally.
- Glass panels use a single consistent blur/opacity recipe everywhere
  rather than bespoke values per component.
