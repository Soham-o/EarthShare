# EarthShare — Architecture

## Layered backend (Clean Architecture)

```
API layer        app/api/v1/*.py        — HTTP concerns only: parse request,
                                           call a service, shape the response.
                                           No business logic, no SQL.
Service layer     app/services/*.py     — business rules: the carbon engine,
                                           dividend math, auth rules, insight
                                           generation. Pure where possible
                                           (carbon_engine has zero I/O).
Repository layer  app/repositories/*.py — the only place SQLAlchemy queries
                                           are written. Services depend on
                                           repository interfaces, never on
                                           the ORM directly.
Data layer        app/models/*.py       — SQLAlchemy table definitions.
```

Dependency direction is strictly one-way: API → Service → Repository →
Model. A service never imports from `app.api`, and a repository never
imports from `app.services`. This is what makes the carbon engine and
auth service unit-testable with zero database and zero HTTP server (see
`tests/test_carbon_engine.py`, `tests/test_auth.py`).

Dependency injection is FastAPI's `Depends()` throughout: `get_db` yields
a request-scoped session, `get_current_user` resolves and validates the
JWT into a `User`, and every route declares exactly what it needs as a
function parameter — nothing is reached for via globals.

## Request flow (example: GET /api/v1/dashboard)

```
Client (Next.js)
  → fetch with Authorization: Bearer <jwt>
  → FastAPI route (app/api/v1/dashboard.py)
      → get_current_user dependency verifies JWT, loads User
      → FootprintRepository.latest() / .history()
      → ActionCompletionRepository.list_for_user()
      → dashboard_service.build_dashboard() — pure computation
  ← DashboardResponse (Pydantic-validated JSON)
  → React renders EquityRing + charts from typed response
```

## Frontend structure

```
src/app/            Next.js App Router pages (one folder per route)
src/components/ui/  Generic primitives: Button, Card, Field, Badge
src/components/...  Feature-specific composites (dashboard, onboarding,
                     marketplace, progress)
src/lib/            api.ts (typed fetch client), auth-context.tsx
                     (token + user state), types.ts (mirrors backend
                     Pydantic schemas by hand — see note below), hooks.ts
```

Every page is a client component that calls the typed `api` client via
the shared `useAuthedFetch` hook, with a loading state, an error state,
and a populated state — no page silently shows nothing on failure.

**Note on type duplication:** `src/lib/types.ts` is hand-written to match
the backend's Pydantic schemas rather than generated from the OpenAPI
spec. For an MVP this is the lower-risk choice (no extra build step that
could fail during a live demo); for a production system the next step
would be generating these from `/openapi.json` (e.g. via `openapi-typescript`)
so the two can't drift silently.

## Why these specific architecture choices for a hackathon timeline

- **Repository pattern** earns its keep immediately: it's what let the
  entire test suite run against an in-memory SQLite database with zero
  changes to service code, and is the seam where Postgres slots in later.
- **Service layer as the unit-test surface** means the most
  judge-relevant logic (the carbon engine, the dividend formula) has
  direct, fast, dependency-free tests instead of only being exercised
  indirectly through API tests.
- **No premature abstraction beyond this** — there's no event bus, no
  CQRS, no microservices. Those would cost build time without buying
  anything a single-team MVP judged in one sitting actually needs.
