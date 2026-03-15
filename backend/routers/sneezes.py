from datetime import datetime
from typing import Annotated

from dependencies import AuthInfo, verify_access_token
from domains.sneeze.models import (CreateSneezeRequest, Sneeze,
                                   UpdateSneezeRequest)
from fastapi import APIRouter, Depends, HTTPException, status

from infrastructure.persistence.sneeze_repository import (
    repo_create_sneeze,
    repo_delete_sneeze,
    repo_get_all_sneezes_by_user_id,
    repo_get_sneeze_by_id,
    repo_update_sneeze,
)

router = APIRouter(
    prefix="/sneezes",
    tags=["sneezes"],
    dependencies=[Depends(verify_access_token)],
    responses={404: {"description": "Not found"}},
)

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

    sneeze = Sneeze(
        user_id=auth.sub,
        notes=body.notes,
        occurred_at=body.occurred_at if body.occurred_at is not None else datetime.now(),
        location=body.location,
        volume=body.volume,
    )
    return repo_create_sneeze(sneeze)


@router.get(
    "/",
    summary="List sneezes",
)
async def list_sneezes(auth: Annotated[AuthInfo, Depends(verify_access_token)]) -> list[Sneeze]:
    """Return all sneezes (order not guaranteed; add query params for filtering later)."""
    return repo_get_all_sneezes_by_user_id(auth.sub)


@router.get(
    "/{sneeze_id}",
    summary="Get sneeze by ID",
)
async def get_sneeze(sneeze_id: str) -> Sneeze:
    """Return a single sneeze by ID."""
    try:
        return repo_get_sneeze_by_id(sneeze_id)
    except ValueError as e:
        handle_value_error(e)


@router.put(
    "/{sneeze_id}",
    summary="Update a sneeze",
)
async def update_sneeze(sneeze_id: str, body: UpdateSneezeRequest) -> Sneeze:
    """Update an existing sneeze."""
    try:
        return repo_update_sneeze(sneeze_id, body)
    except ValueError as e:
        handle_value_error(e)

@router.delete(
    "/{sneeze_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a sneeze",
)
async def delete_sneeze(sneeze_id: str) -> None:
    """Delete a sneeze by ID."""
    try:
        repo_delete_sneeze(sneeze_id)
    except ValueError as e:
        handle_value_error(e)

def handle_value_error(e: ValueError) -> None:
    if "not found" in str(e):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Sneeze not found")
    else:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")