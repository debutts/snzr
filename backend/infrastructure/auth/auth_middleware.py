from fastapi import HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jwt_validator import validate_jwt, create_auth_info
import os

# todo update how we get this : https://docs.logto.io/authorization/validate-access-tokens#fetch-from-openid-connect-discovery-endpoint
LOGTO_TENANT_URL = os.environ['LOGTO_TENANT_URL']
JWKS_URI = LOGTO_TENANT_URL +'/oidc/jwks'
ISSUER = LOGTO_TENANT_URL + '/oidc'

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

security = HTTPBearer()

async def verify_access_token(credentials: HTTPAuthorizationCredentials = Depends(security)) -> AuthInfo:
    try:
        token = credentials.credentials
        payload = validate_jwt(token)
        return create_auth_info(payload)

    except AuthorizationError as e:
        raise HTTPException(status_code=e.status, detail=str(e))