"""FastAPI dependencies. Re-export Logto auth for convenience."""
from infrastructure.auth import (AuthInfo, verify_access_token)

__all__ = [
    "AuthInfo",
    "verify_access_token"
]
