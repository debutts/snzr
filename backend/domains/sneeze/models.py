from datetime import datetime
from typing import Optional
from uuid import uuid4

from pydantic import BaseModel
from sqlmodel import Field, Relationship, SQLModel

from backend.domains.tag.models import Tag

class SneezeTagLink(SQLModel, table=True):
    id: str = Field(default_factory=lambda: str(uuid4()), primary_key=True)
    sneezeId = str = Field(foreign_key="sneeze.id", index=True)
    tagId = str = Field(foreign_key="tag.id", index=True)

class Sneeze(SQLModel, table=True):
    id: str = Field(default_factory=lambda: str(uuid4()), primary_key=True)
    user_id: str
    notes: Optional[str] = Field(default=None, max_length=1000)
    occurred_at: datetime = Field(default_factory=datetime.now)
    location: Optional[str] = Field(default=None, max_length=1000)
    volume: Optional[int] = Field(default=None, ge=0, le=10)
    tags: list["Tag"] = Relationship(back_populates="tags", link_model=SneezeTagLink)
