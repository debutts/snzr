"""Logto JWT verification config. Load from env so React app and FastAPI share the same tenant."""
import os

LOGTO_ENDPOINT = os.getenv("LOGTO_ENDPOINT", "").rstrip("/")
"""Logto tenant URL, e.g. https://your-tenant.logto.app."""

ISSUER = f"{LOGTO_ENDPOINT}/oidc" if LOGTO_ENDPOINT else ""
"""Expected JWT issuer (Logto OIDC URL)."""

JWKS_URI = f"{LOGTO_ENDPOINT}/oidc/jwks" if LOGTO_ENDPOINT else ""
"""JWKS URL for verifying Logto-signed JWTs."""

# Optional: for global API resource protection (audience + scope checks)
LOGTO_API_RESOURCE = os.getenv("LOGTO_API_RESOURCE", "")
"""API resource indicator (audience). If set, tokens must include this in `aud`."""

LOGTO_REQUIRED_SCOPES = [
    s.strip() for s in os.getenv("LOGTO_REQUIRED_SCOPES", "").split(",") if s.strip()
]
"""Required scopes for protected routes. If empty, scope check is skipped."""
