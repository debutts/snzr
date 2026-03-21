"""Tests for sneeze_repository (SQLite via patch_engines)."""

from __future__ import annotations

from datetime import datetime, timezone

import pytest
from domains.sneeze.models import Sneeze
from domains.sneeze.requests import UpdateSneezeRequest
from infrastructure.persistence.sneeze_repository import (
    repo_create_sneeze, repo_delete_sneeze,
    repo_get_all_sneezes_by_tag_and_user, repo_get_all_sneezes_by_user_id,
    repo_get_sneeze_by_id, repo_update_sneeze)

USER_A = "user-a"
USER_B = "user-b"


@pytest.fixture
def sneeze_factory(patch_engines):
    """Create sneezes."""

    def _make(
        *,
        user_id: str = USER_A,
        notes: str | None = "note",
        tag_names: list[str] | None = None,
        occurred_at: datetime | None = None,
    ) -> Sneeze:
        sneeze = Sneeze(
            user_id=user_id,
            notes=notes,
            occurred_at=occurred_at or datetime(2024, 6, 1, 12, 0, 0, tzinfo=timezone.utc),
            location="here",
            volume=5,
        )
        return repo_create_sneeze(sneeze, tag_names=tag_names)

    return _make


def test_repo_create_with_tags(sneeze_factory):
    s = sneeze_factory(tag_names=["Alpha", "beta"])
    assert s.id
    assert {t.name for t in s.tags} == {"alpha", "beta"}


def test_repo_get_by_id(sneeze_factory):
    created = sneeze_factory(notes="one")
    loaded = repo_get_sneeze_by_id(created.id, USER_A)
    assert loaded.id == created.id
    assert loaded.notes == "one"


def test_repo_get_by_id_not_found(sneeze_factory):
    sneeze_factory()
    with pytest.raises(ValueError, match="not found"):
        repo_get_sneeze_by_id("00000000-0000-0000-0000-000000000000", USER_A)


def test_repo_get_by_id_wrong_user_raises_permission(sneeze_factory):
    created = sneeze_factory(user_id=USER_A)
    with pytest.raises(PermissionError):
        repo_get_sneeze_by_id(created.id, USER_B)


def test_repo_list_by_user_orders_newest_first(sneeze_factory):
    first = sneeze_factory(
        notes="older",
        occurred_at=datetime(2020, 1, 1, tzinfo=timezone.utc),
    )
    second = sneeze_factory(
        notes="newer",
        occurred_at=datetime(2025, 1, 1, tzinfo=timezone.utc),
    )
    rows = repo_get_all_sneezes_by_user_id(USER_A)
    assert [r.id for r in rows] == [second.id, first.id]


def test_repo_list_by_tag(sneeze_factory):
    sneeze_factory(tag_names=["shared", "x"])
    sneeze_factory(tag_names=["other"])
    rows = repo_get_all_sneezes_by_tag_and_user("Shared", USER_A)
    assert len(rows) == 1
    assert {t.name for t in rows[0].tags} >= {"shared"}


def test_repo_update(sneeze_factory):
    created = sneeze_factory(tag_names=["t1"])
    body = UpdateSneezeRequest(
        notes="updated",
        occurred_at=datetime(2024, 7, 1, tzinfo=timezone.utc),
        location="there",
        volume=3,
        tag_names=["t2"],
    )
    out = repo_update_sneeze(created.id, USER_A, body)
    assert out.notes == "updated"
    assert {t.name for t in out.tags} == {"t2"}


def test_repo_delete(sneeze_factory):
    created = sneeze_factory()
    repo_delete_sneeze(created.id, USER_A)
    with pytest.raises(ValueError, match="not found"):
        repo_get_sneeze_by_id(created.id, USER_A)
