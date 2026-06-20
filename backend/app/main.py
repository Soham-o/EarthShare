from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from app.api.v1 import actions, auth, checkin, dashboard, insights, onboarding, progress
from app.core.config import get_settings
from app.core.database import init_db
from app.core.limiter import limiter

settings = get_settings()

# Tight CSP for the JSON API — no HTML, no scripts, frame-ancestors none.
_API_CSP = "default-src 'none'; frame-ancestors 'none'"


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


app = FastAPI(
    title=settings.app_name,
    version="1.0.0",
    description="EarthShare API — track, understand, and reduce your carbon footprint.",
    lifespan=lifespan,
)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

print("CORS ORIGINS:", settings.cors_origin_list)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origin_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def security_headers(request: Request, call_next):
    response = await call_next(request)

    # Only enable CSP in production
    if settings.is_production:
        response.headers["Content-Security-Policy"] = _API_CSP
        response.headers["Strict-Transport-Security"] = (
            "max-age=63072000; includeSubDomains"
        )

    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    response.headers["Permissions-Policy"] = (
        "geolocation=(), microphone=(), camera=()"
    )

    return response


@app.exception_handler(Exception)
async def unhandled_exception_handler(request: Request, exc: Exception):
    """Never leak internals — log server-side, return a generic 500."""
    import logging

    logging.exception("Unhandled exception on %s %s", request.method, request.url.path)
    return JSONResponse(status_code=500, content={"detail": "Internal server error."})


@app.get("/health", tags=["health"])
def health():
    return {"status": "ok"}


app.include_router(auth.router)
app.include_router(onboarding.router)
app.include_router(dashboard.router)
app.include_router(insights.router)
app.include_router(actions.router)
app.include_router(progress.router)
app.include_router(checkin.router)

print("REGISTERED ROUTES:")
for route in app.routes:
    print(route.path)
