"""Validate Logto-issued JWTs and build AuthInfo. See https://docs.logto.io/authorization/validate-access-tokens."""
from typing import Any

import jwt
from jwt import PyJWKClient

from .config import ISSUER, JWKS_URI, LOGTO_API_RESOURCE, LOGTO_REQUIRED_SCOPES
from .models import LogToAuthInfo


class AuthorizationError(Exception):
    """Raised when token is missing, invalid, or lacks required permissions."""

    def __init__(self, message: str, status: int = 401) -> None:
        self.message = message
        self.status = status
        super().__init__(self.message)


def _get_jwks_client() -> PyJWKClient:
    if not JWKS_URI:
        raise AuthorizationError(
            "LOGTO_ENDPOINT is not set; cannot verify JWTs",
            status=503,
        )
    return PyJWKClient(JWKS_URI)


def validate_jwt(token: str) -> dict[str, Any]:
    """Verify JWT signature and standard claims; optionally audience and scopes. Returns payload."""
    jwks_client = _get_jwks_client()
    try:
        signing_key = jwks_client.get_signing_key_from_jwt(token)
        payload = jwt.decode(
            token,
            signing_key.key,
            algorithms=["RS256"],
            issuer=ISSUER,
            options={"verify_aud": False},
        )
    except jwt.InvalidTokenError as e:
        raise AuthorizationError(f"Invalid token: {e!s}", 401) from e

    _verify_payload(payload)
    return payload


def _verify_payload(payload: dict[str, Any]) -> None:
    """Enforce audience and scope if configured (global API resource model)."""
    if LOGTO_API_RESOURCE:
        aud = payload.get("aud") or []
        audiences = [aud] if isinstance(aud, str) else aud
        if LOGTO_API_RESOURCE not in audiences:
            raise AuthorizationError("Invalid audience", 403)

    if LOGTO_REQUIRED_SCOPES:
        scope_str = payload.get("scope") or ""
        scopes = scope_str.split() if isinstance(scope_str, str) else []
        missing = [s for s in LOGTO_REQUIRED_SCOPES if s not in scopes]
        if missing:
            raise AuthorizationError(f"Insufficient scope: missing {missing}", 403)


def create_auth_info(payload: dict[str, Any]) -> LogToAuthInfo:
    """Build AuthInfo from validated JWT payload."""
    scope_str = payload.get("scope") or ""
    scopes = scope_str.split() if isinstance(scope_str, str) else []

    aud = payload.get("aud")
    audience = [aud] if isinstance(aud, str) else (aud or [])

    roles = payload.get("roles")
    if isinstance(roles, str):
        roles = [roles]
    roles = roles or []

    return LogToAuthInfo(
        sub=payload.get("sub", ""),
        client_id=payload.get("client_id"),
        organization_id=payload.get("organization_id"),
        scopes=scopes,
        audience=audience,
        roles=roles,
    )
