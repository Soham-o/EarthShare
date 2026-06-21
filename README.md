# 🌍 EarthShare

**Own a Share of the Planet.**

### Built for the Carbon Footprint Awareness Platform Challenge

---

## Ⅰ. The Paradigm Shift

Most sustainability products fail because they focus entirely on information. They treat sustainability as an exercise in guilt. Users see an abstract number—a "carbon footprint"—they feel bad, and nothing changes.

EarthShare introduces a fundamentally different mental model based on behavioral psychology:

> **Information creates awareness. Ownership creates responsibility.**
> People do not protect what they consume. They protect what they own.

Instead of showing users a carbon footprint score alone, EarthShare gives them a symbolic share in the future of the planet. Every sustainable action becomes an investment. Every reduction becomes ownership.

Behavior change is the real climate technology.

---

## 🚀 Live Environment

---

## Ⅱ. The Product Experience

EarthShare is a fully functional, production-ready platform featuring a complete user journey from assessment to habitual action.

### 🎯 Smart Onboarding & Assessment

A frictionless, beautifully designed assessment engine evaluating footprints across 5 core categories:

* **Food**
* **Home Energy**
* **Transport**
* **Shopping**
* **Long-distance Travel**

### 📊 The Equity Dashboard

A real-time translation of emissions into equity:

* **Carbon Score & EarthShare Dividend:** Your quantified planetary equity.
* **Future Projection:** Deterministic modeling of your current trajectory vs. optimized trajectory.
* **Reduction Potential:** Gamified targets based on actionable insights.
* **Category Breakdown:** Highly personalized, color-safe visual metrics powered by Recharts.

### 🧠 Personalized Intelligence

* **Behavioral Analysis:** Deep dives into your specific consumption patterns.
* **AI-Enhanced Insight Generation:** Context-aware, empathetic recommendations utilizing an optional Gemini Enhancement Layer.
* **Weekly Action Plan:** Algorithmic opportunity identification tailored to your lifestyle.

### 🛒 The Sustainability Marketplace

Users don't just read advice; they "purchase" real sustainability actions (e.g., *Public transport, Food waste reduction, Local produce, Energy saving, Carpooling, Plant-based alternatives*).
Each action is mathematically weighted by:

* **Carbon Savings**
* **Difficulty**
* **Impact Score**

### 📈 Progress Loop

* **Weekly Trend Visualization:** Longitudinal tracking of CO₂ saved.
* **Achievement Badges & Action History:** A continuous habit-building system.

---

## Ⅲ. Competitive Advantage

| Feature | Traditional Carbon Calculators | EarthShare 🌍 |
| --- | --- | --- |
| **Mental Model** | Reports emissions (Guilt) | Creates ownership (Equity) |
| **Output Type** | Static reports | Dynamic action marketplace |
| **Guidance** | Generic advice ("Drive less") | Highly personalized, algorithmic insights |
| **Retention** | Calculate once and abandon | Continuous habit-building system |
| **Motivation** | Abstract numbers | Gamified EarthShare Dividends |

---

## Ⅳ. Engineering Decisions

**Why deterministic calculations?**

Carbon scores should be:
* Reproducible
* Explainable
* Auditable

AI is used only for interpretation and guidance, not for the underlying carbon calculations. We explicitly chose a deterministic architecture for the core math to ensure that a specific lifestyle change yields the exact same dividend every time, creating absolute transparency for the user.

---

## Ⅴ. Code Quality

EarthShare follows a layered architecture:

* **Presentation Layer** (Next.js)
* **API Layer** (FastAPI)
* **Service Layer**
* **Repository Layer**
* **Data Layer**

This separation enables:
* Testability
* Maintainability
* Scalability
* Clear ownership of business logic


+-------------------------------------------------------------+
|                    PRESENTATION LAYER                       |
|  Next.js 15 | TypeScript | Tailwind CSS | Recharts (Vercel) |
+------------------------------+------------------------------+
                               | HTTP / REST
+------------------------------v------------------------------+
|                    INFRASTRUCTURE LAYER                     |
|    FastAPI Gateway | JWT Auth | CORS | Rate Limiting        |
+------------------------------+------------------------------+
                               |
+------------------------------v------------------------------+
|                   BUSINESS LOGIC LAYER                      |
|  Carbon Intelligence Engine | AI Enhancement (Gemini)       |
|  Behavioral Analytics       | Action & Dividend Calculator  |
+------------------------------+------------------------------+
                               |
+------------------------------v------------------------------+
|                    PERSISTENCE LAYER                        |
|  SQLAlchemy ORM | SQLite (Postgres-Ready) | Render Hosted   |
+-------------------------------------------------------------+

Ⅵ. Security
EarthShare implements strict security standards at the gateway and application levels:

JWT Authentication

Password hashing

Input validation using Pydantic

CORS protection

Rate limiting

Secure HTTP headers

Principle of least privilege

Ⅶ. Testing
We didn't just build a prototype; we built a tested application.

Backend:

61 pytest tests

Unit tests

Integration tests

Frontend:

Vitest

Accessibility testing

Coverage target: 80%+ (Currently achieving 96%)

Ⅷ. Accessibility
EarthShare is designed to be accessible. We believe climate technology must be usable by everyone.

Keyboard navigation

ARIA labels

Screen-reader support

Responsive design

WCAG-conscious color palette

Ⅸ. Interface Showcase

## 📸 Product Walkthrough



<p align="center">

  <img src="https://raw.githubusercontent.com/Soham-o/EarthShare/main/docs/screenshots/dashboard.png" width="48%">

  <img src="https://raw.githubusercontent.com/Soham-o/EarthShare/main/docs/screenshots/insights.png" width="48%">

</p>



<p align="center">

  <img src="https://raw.githubusercontent.com/Soham-o/EarthShare/main/docs/screenshots/marketplace.png" width="48%">

  <img src="https://raw.githubusercontent.com/Soham-o/EarthShare/main/docs/screenshots/progress.png" width="48%">

</p>

---

Ⅹ. Future Roadmap
EarthShare's architecture is designed to scale from an individual habit-tracker to a global sustainability network:

Community EarthShares: Aggregate planetary equity across neighborhoods or cities.

Team Sustainability Challenges: B2B integration allowing companies to run internal environmental impact sprints.

Smart Utility Integrations: Automated API connections to home energy providers for real-time footprint adjustments.

Verified Impact Marketplace: Evolving actions from self-reported data to verified environmental assets.

AI Sustainability Coach: Expanding the Gemini integration into a conversational agent that negotiates daily micro-habits with the user.
