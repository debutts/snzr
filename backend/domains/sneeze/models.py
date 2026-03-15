from datetime import datetime
from typing import Optional
from uuid import uuid4

from pydantic import BaseModel
from sqlmodel import Field, SQLModel


class Sneeze(SQLModel, table=True):
    id: str = Field(default_factory=lambda: str(uuid4()), primary_key=True)
    user_id: str
    notes: Optional[str] = Field(default=None, max_length=1000)
    occurred_at: datetime = Field(default_factory=datetime.now)
    location: Optional[str] = Field(default=None, max_length=1000)
    volume: Optional[int] = Field(default=None, ge=0, le=10)


class CreateSneezeRequest(BaseModel):
    """Request body for creating a sneeze. All fields optional; occurred_at defaults to now."""

    notes: Optional[str] = Field(default=None, max_length=1000)
    occurred_at: Optional[datetime] = None
    location: Optional[str] = Field(default=None, max_length=1000)
    volume: Optional[int] = Field(default=None, ge=0, le=10)


class UpdateSneezeRequest(BaseModel):
    """Request body for updating a sneeze. All fields optional."""

    notes: Optional[str] = Field(default=None, max_length=1000)
    occurred_at: datetime
    location: Optional[str] = Field(default=None, max_length=1000)
    volume: Optional[int] = Field(default=None, ge=0, le=10)
