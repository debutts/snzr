from datetime import datetime
from typing import Optional
from uuid import uuid4

from domains.tag.models import Tag
from sqlmodel import Field, Relationship, SQLModel


class SneezeTagLink(SQLModel, table=True):
    id: str = Field(default_factory=lambda: str(uuid4()), primary_key=True)
    sneeze_id: str = Field(foreign_key="sneeze.id", index=True)
    tag_id: str = Field(foreign_key="tag.id", index=True)

class Sneeze(SQLModel, table=True):
    id: str = Field(default_factory=lambda: str(uuid4()), primary_key=True)
    user_id: str
    notes: Optional[str] = Field(default=None, max_length=1000)
    occurred_at: datetime = Field(default_factory=datetime.now)
    location: Optional[str] = Field(default=None, max_length=1000)
    volume: Optional[int] = Field(default=None, ge=0, le=10)
    tags: list[Tag] = Relationship(
        link_model=SneezeTagLink,
        sa_relationship_kwargs={"lazy": "joined"},
    )
