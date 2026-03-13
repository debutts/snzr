from pydantic import BaseModel


class Sneeze(BaseModel):
    """Full sneeze response model."""

    id: str
    user_id: str
    notes: str | None = None
    occurred_at: datetime
    location: str | None = None
    volume: int | None = None


class CreateSneezeRequest(BaseModel):
    """Request body for creating a sneeze. All fields optional; occurred_at defaults to now."""

    notes: str | None = None
    occurred_at: datetime | None = None
    location: str | None = None
    volume: int | None = None


class UpdateSneezeRequest(BaseModel):
    """Request body for updating a sneeze. All fields optional."""

    notes: str | None = None
    occurred_at: datetime
    location: str | None = None
    volume: int | None = None
