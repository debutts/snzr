import os

from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jwt_validator import create_auth_info, validate_jwt

# When True, no Bearer token is required; a dev AuthInfo is used. For local dev/testing only.
_DISABLE_AUTH = os.environ.get("DISABLE_AUTH", "").lower() in ("1", "true")

# Only required when auth is enabled
LOGTO_TENANT_URL = os.environ.get("LOGTO_TENANT_URL", "")
JWKS_URI = LOGTO_TENANT_URL + "/oidc/jwks" if LOGTO_TENANT_URL else ""
ISSUER = LOGTO_TENANT_URL + "/oidc" if LOGTO_TENANT_URL else ""

class AuthInfo:
    def __init__(self, sub: str, client_id: str = None, organization_id: str = None,
                 scopes: list = None, audience: list = None):
        self.sub = sub
        self.client_id = client_id
        self.organization_id = organization_id
        self.scopes = scopes or []
        self.audience = audience or []

    def to_dict(self):
        return {
            'sub': self.sub,
            'client_id': self.client_id,
            'organization_id': self.organization_id,
            'scopes': self.scopes,
            'audience': self.audience
        }

class AuthorizationError(Exception):
    def __init__(self, message: str, status: int = 403):
        self.message = message
        self.status = status
        super().__init__(self.message)

# Optional so we can skip the header when DISABLE_AUTH is set
security = HTTPBearer(auto_error=False)

# Mock identity used when auth is disabled (local dev/testing)
DEV_AUTH_INFO = AuthInfo(
    sub="dev-user",
    client_id="dev-client",
    scopes=["snzr.read", "snzr.write"],
    audience=[],
)


def verify_access_token(
    credentials: HTTPAuthorizationCredentials | None = Depends(security),
) -> AuthInfo:
    if _DISABLE_AUTH:
        return DEV_AUTH_INFO
    if not LOGTO_TENANT_URL:
        raise HTTPException(
            status_code=500,
            detail="LOGTO_TENANT_URL must be set when auth is enabled",
        )
    if credentials is None:
        raise HTTPException(
            status_code=401,
            detail="Missing or invalid authorization header",
        )
    try:
        token = credentials.credentials
        payload = validate_jwt(token)
        return create_auth_info(payload)
    except AuthorizationError as e:
        raise HTTPException(status_code=e.status, detail=str(e))