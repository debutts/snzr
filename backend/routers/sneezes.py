from datetime import datetime, timezone
from typing import Annotated
from uuid import uuid4

from fastapi import APIRouter, Depends, HTTPException, status

from dependencies import AuthInfo, verify_access_token
from domains.sneeze.models import (CreateSneezeRequest, Sneeze,
                                   UpdateSneezeRequest)

router = APIRouter(
    prefix="/sneezes",
    tags=["sneezes"],
    dependencies=[Depends(verify_access_token)],
    responses={404: {"description": "Not found"}},
)

# ---------------------------------------------------------------------------
# In-memory store (replace with DB later)
# ---------------------------------------------------------------------------

fake_sneezes_db: dict[str, Sneeze] = {}


def _now_utc() -> datetime:
    return datetime.now(timezone.utc)


# ---------------------------------------------------------------------------
# CRUD endpoints
# ---------------------------------------------------------------------------


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    summary="Create a sneeze",
)
async def create_sneeze(
    body: CreateSneezeRequest,
    auth: Annotated[AuthInfo, Depends(verify_access_token)],
) -> Sneeze:
    """Create a new sneeze. If `occurred_at` is not provided, it defaults to now (UTC)."""
    occurred_at = body.occurred_at if body.occurred_at is not None else _now_utc()
    sneeze = Sneeze(
        id=str(uuid4()),
        user_id=auth.sub,
        notes=body.notes,
        occurred_at=occurred_at,
        location=body.location,
        volume=body.volume,
    )
    fake_sneezes_db[sneeze.id] = sneeze
    return sneeze


@router.get(
    "/",
    summary="List sneezes",
)
async def list_sneezes() -> list[Sneeze]:
    """Return all sneezes (order not guaranteed; add query params for filtering later)."""
    return list(fake_sneezes_db.values())


@router.get(
    "/{sneeze_id}",
    summary="Get sneeze by ID",
)
async def get_sneeze(sneeze_id: str) -> Sneeze:
    """Return a single sneeze by ID."""
    if sneeze_id not in fake_sneezes_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
        )
    return fake_sneezes_db[sneeze_id]


@router.put(
    "/{sneeze_id}",
    summary="Update a sneeze",
)
async def update_sneeze(sneeze_id: str, body: UpdateSneezeRequest) -> Sneeze:
    """Update an existing sneeze."""
    if sneeze_id not in fake_sneezes_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
        )
    existing = fake_sneezes_db[sneeze_id]
    updated = Sneeze(
        id=existing.id,
        user_id=existing.user_id,
        notes=body.notes,
        occurred_at=body.occurred_at,
        location=body.location,
        volume=body.volume,
    )
    fake_sneezes_db[sneeze_id] = updated
    return updated


@router.delete(
    "/{sneeze_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a sneeze",
)
async def delete_sneeze(sneeze_id: str) -> None:
    """Delete a sneeze by ID."""
    if sneeze_id not in fake_sneezes_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
        )
    del fake_sneezes_db[sneeze_id]
