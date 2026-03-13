"""FastAPI dependencies for Logto JWT Bearer auth."""
from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from .jwt_validator import AuthorizationError, create_auth_info, validate_jwt
from .models import LogToAuthInfo

security = HTTPBearer(auto_error=True)


async def get_logto_auth(
    credentials: HTTPAuthorizationCredentials = Depends(security),
) -> LogToAuthInfo:
    """
    Validate Authorization: Bearer <token> and return AuthInfo (sub, scopes, roles, etc.).
    Use as a dependency on protected routes.
    """
    try:
        payload = validate_jwt(credentials.credentials)
        return create_auth_info(payload)
    except AuthorizationError as e:
        raise HTTPException(status_code=e.status, detail=e.message) from e


def require_scopes(*scopes: str):
    """Return a dependency that requires the user to have all of the given scopes."""

    async def _require(auth: LogToAuthInfo = Depends(get_logto_auth)) -> LogToAuthInfo:
        missing = [s for s in scopes if s not in auth.scopes]
        if missing:
            raise HTTPException(
                status_code=403,
                detail=f"Insufficient scope: missing {missing}",
            )
        return auth

    return Depends(_require)


def require_roles(*roles: str):
    """Return a dependency that requires the user to have at least one of the given roles."""

    async def _require(auth: LogToAuthInfo = Depends(get_logto_auth)) -> LogToAuthInfo:
        if not roles:
            return auth
        if not any(r in auth.roles for r in roles):
            raise HTTPException(
                status_code=403,
                detail=f"Insufficient role: need one of {list(roles)}",
            )
        return auth

    return Depends(_require)
