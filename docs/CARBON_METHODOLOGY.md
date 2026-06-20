# Carbon Calculation Methodology

EarthShare's carbon engine (`backend/app/services/carbon_engine.py`) is a
**local, deterministic, rule-based model** — no external API, no network
call, no randomness. Given the same onboarding answers, it always returns
the same footprint and score. That's a product requirement, not just an
engineering nicety: the entire "ownership" framing falls apart if a user's
score can drift without their behavior changing.

## Why rule-based, not ML

A hackathon weekend is not enough time to source, clean, and validate a
real emissions dataset per-user, and a model trained on too little data
would be *less* trustworthy than transparent arithmetic. A rule-based
model that's wrong is at least wrong in a way you can read, audit, and
fix in one line. That's the right trade-off for this stage.

## The five inputs

| Category | Levels | What it captures |
|---|---|---|
| Transport | car, bus, train, bike, walking | Daily commute mode |
| Food | vegetarian, mixed, meat_heavy | Diet pattern |
| Energy | low, medium, high | Home heating/cooling/appliance use |
| Shopping | low, medium, high | Frequency of new-goods purchases |
| Travel | rare, monthly, frequent | Long-distance trips / flights |

## Emission factors (kg CO2-equivalent per month)

These are simplified, order-of-magnitude figures in the spirit of widely
published per-capita averages (EPA- and Our-World-in-Data-style estimates
for a developed-economy individual), deliberately rounded for an
explainable MVP model rather than a verified life-cycle assessment:

```
Transport:  car=180   bus=70   train=45   bike=5   walking=2
Food:       vegetarian=110   mixed=210   meat_heavy=290
Energy:     low=60   medium=140   high=260
Shopping:   low=30   medium=80   high=160
Travel:     rare=15   monthly=90   frequent=220
```

**Total** = sum of the five selected factors. This is intentionally a
flat sum, not a weighted or interacting model — addition is auditable;
a hidden interaction term is not.

## Carbon Score (0–1000, higher is better)

```
score = 1000 × (1 − clamp((total − 150) / (1000 − 150), 0, 1))
```

Linear between two calibration anchors: a footprint at or below 150
kg/month scores 1000 (best realistic case is ~104 kg, with bike +
vegetarian + low + low + rare); a footprint at or above 1000 kg/month
scores 0 (worst realistic case is ~930 kg, with car + meat_heavy + high
+ high + frequent). Linear and monotonic was chosen over a more
"realistic" curve specifically so the score is easy to explain in one
sentence to a user or a judge.

## EarthShare Dividend & Shares

- **Dividend points** = `max(0, national_average − your_total) × 0.8`
  `+ (cumulative kg saved from completed actions) × 0.5`
- **Shares** = `1 + floor(cumulative kg saved / 5)` — every user starts
  owning 1 share; completing actions mints more.

These are explicitly gamification constants, not a real carbon price —
documented here so the conversion is never a mystery.

## Reduction potential & improved projection

- **Reduction potential** = sum of `kg_co2_saved_month` across all
  not-yet-completed marketplace actions.
- **Improved projection** = `(total − sum of your top 2 highest-impact
  uncompleted actions) × 12`, i.e. "what your year looks like if you do
  the two most effective things available to you."

## National average benchmark

660 kg CO2/month is used only as a comparison anchor in the dashboard and
insights copy (e.g. "12% below average") — it never affects the score or
dividend calculation directly except through the dividend formula above.

## Known simplifications (by design, for an MVP)

- No regional/country-specific emission factors (a flight from a 50 kWh
  vs 2,000 kWh electricity grid produces very different real emissions).
- No granularity within a level (e.g. "car" doesn't distinguish an EV
  from a pickup truck).
- Travel is amortized to a flat monthly figure rather than tracking
  individual trips.

Each of these is a deliberate "MVP boundary," not an oversight — the
brief asked for a working, explainable prototype, not a verified LCA
tool, and every constant above is named, sourced-in-spirit, and isolated
in one file specifically so it can be refined later without touching
anything else in the codebase.
