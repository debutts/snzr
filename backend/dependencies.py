"""FastAPI dependencies. Re-export Logto auth for convenience."""
from infrastructure.auth import (LogToAuthInfo, get_logto_auth, require_roles,
                                 require_scopes)

__all__ = [
    "LogToAuthInfo",
    "get_logto_auth",
    "require_roles",
    "require_scopes",
]
