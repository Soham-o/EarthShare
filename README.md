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

## Ⅳ. Engineering Highlights

EarthShare was engineered with the rigor of a leading SaaS platform. It strictly separates concerns, ensuring scalability, testability, and security.

### System Architecture

```text
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

```

### ⚙️ Deterministic Carbon Intelligence Engine

At the core of EarthShare is our proprietary scoring model. We explicitly chose a **deterministic architecture** rather than a pure black-box AI model for the core calculations.

* **Transparency:** Users must understand exactly *why* their score changed.
* **Reproducibility:** A specific lifestyle change must yield the exact same dividend every time.
* **AI as an Enhancement:** The Gemini LLM acts as an optional interpretation layer—translating deterministic math into highly empathetic, personalized human insights.

### 🔐 Security Hardened

* Robust **JWT Authentication** and secure password hashing.
* Strict **Input Validation** via Pydantic.
* **CORS Protection**, rate limiting, and secure HTTP headers at the gateway level.

### ♿ Accessibility First

We built EarthShare for everyone.

* Full **Keyboard Navigation** and deep **Screen-Reader Support**.
* Comprehensive **ARIA labels** across all interactive elements.
* **Color-safe visualization** palettes passing WCAG contrast requirements.
* Flawlessly **Responsive Design** across mobile, tablet, and desktop.

---

## Ⅴ. Launch & Submission Metrics

We didn't just build a prototype; we built a tested, production-grade application.

* **Testing Infrastructure:** 61 robust backend unit and integration tests powered by `pytest`, coupled with frontend state validation via `vitest`.
* **CI/CD Ready:** Production builds passing locally and seamlessly deployed across Vercel and Render.

---

## Ⅵ. Interface Showcase

---

## Ⅶ. Future Roadmap

EarthShare's architecture is designed to scale from an individual habit-tracker to a global sustainability network:

* **Community EarthShares:** Aggregate planetary equity across neighborhoods or cities.
* **Team Sustainability Challenges:** B2B integration allowing companies to run internal environmental impact sprints.
* **Smart Utility Integrations:** Automated API connections to home energy providers for real-time footprint adjustments.
* **Verified Impact Marketplace:** Evolving actions from self-reported data to verified environmental assets.
* **AI Sustainability Coach:** Expanding the Gemini integration into a conversational agent that negotiates daily micro-habits with the user.

---
