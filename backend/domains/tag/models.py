from uuid import uuid4

from sqlmodel import Field, SQLModel


class Tag(SQLModel, table=True):
    id: str = Field(default_factory=lambda: str(uuid4()), primary_key=True)
    name: str = Field(unique=True, index=True)