"""FastAPI dependencies. Re-export Logto auth for convenience."""
from infrastructure.auth import (AuthInfo, verify_access_token)
from infrastructure.persistence.common.db_engine import create_db_and_tables

__all__ = [
    "AuthInfo",
    "verify_access_token",
    "create_db_and_tables"
]
