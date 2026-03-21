"""API / transport shapes (not tables). Ensures nested `tags` serialize in JSON."""

from datetime import datetime
from typing import Optional

from pydantic import ConfigDict
from sqlmodel import Field, SQLModel


class TagPublic(SQLModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    name: str


class SneezePublic(SQLModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    user_id: str
    notes: Optional[str] = None
    occurred_at: datetime
    location: Optional[str] = None
    volume: Optional[int] = None
    tags: list[TagPublic] = Field(default_factory=list)
