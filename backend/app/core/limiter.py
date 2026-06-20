"""Single shared Limiter instance used across all routers.

Rate limits are env-configured via Settings.rate_limit_default /
Settings.rate_limit_auth so they can be tuned per environment without
a code change (e.g., tighter limits in production, relaxed in staging).
"""
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)
