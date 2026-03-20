from datetime import datetime
from typing import Optional

from pydantic import BaseModel
from sqlmodel import Field

from backend.domains.tag.models import Tag

class CreateSneezeRequest(BaseModel):
    """Request body for creating a sneeze. All fields optional; occurred_at defaults to now."""

    notes: Optional[str] = Field(default=None, max_length=1000)
    occurred_at: Optional[datetime] = None
    location: Optional[str] = Field(default=None, max_length=1000)
    volume: Optional[int] = Field(default=None, ge=0, le=10)
    tags: Optional[list[str]] = Field(default=None)


class UpdateSneezeRequest(BaseModel):
    """Request body for updating a sneeze. All fields will be updated."""

    notes: Optional[str] = Field(default=None, max_length=1000)
    occurred_at: datetime
    location: Optional[str] = Field(default=None, max_length=1000)
    volume: Optional[int] = Field(default=None, ge=0, le=10)
    tags: Optional[list[str]] = Field(default=None)