"""HTTP tests for sneezes router (auth overridden, SQLite via patch_engines)."""

from __future__ import annotations

from datetime import datetime, timezone

import pytest
from dependencies import verify_access_token
from fastapi.testclient import TestClient
from infrastructure.auth import AuthInfo
from main import app

AUTH_SUB = "router-test-user"


@pytest.fixture
def auth_override():
    def _verify() -> AuthInfo:
        return AuthInfo(sub=AUTH_SUB)

    app.dependency_overrides[verify_access_token] = _verify
    yield
    app.dependency_overrides.pop(verify_access_token, None)


@pytest.fixture
def client(patch_engines, auth_override):
    with TestClient(app) as c:
        yield c


def _occurred_iso():
    return datetime(2024, 3, 15, 10, 30, 0, tzinfo=timezone.utc).isoformat()


def test_create_sneeze(client: TestClient):
    res = client.post(
        "/sneezes/",
        json={
            "notes": "api note",
            "occurred_at": _occurred_iso(),
            "location": "desk",
            "volume": 2,
            "tag_names": ["spring", "ALLERGY"],
        },
    )
    assert res.status_code == 201
    data = res.json()
    assert data["notes"] == "api note"
    assert data["user_id"] == AUTH_SUB
    names = {t["name"] for t in data["tags"]}
    assert names == {"spring", "allergy"}


def test_list_mine_empty_then_populated(client: TestClient):
    r0 = client.get("/sneezes/me")
    assert r0.status_code == 200
    assert r0.json() == []

    client.post(
        "/sneezes/",
        json={"notes": "a", "occurred_at": _occurred_iso(), "tag_names": ["t"]},
    )
    r1 = client.get("/sneezes/me")
    assert r1.status_code == 200
    assert len(r1.json()) == 1
    assert r1.json()[0]["notes"] == "a"


def test_get_by_id_404(client: TestClient):
    res = client.get("/sneezes/me/00000000-0000-0000-0000-000000000000")
    assert res.status_code == 404
    assert res.json()["detail"] == "Sneeze not found"


def test_get_by_id_roundtrip(client: TestClient):
    created = client.post(
        "/sneezes/",
        json={"notes": "g", "occurred_at": _occurred_iso()},
    ).json()
    res = client.get(f"/sneezes/me/{created['id']}")
    assert res.status_code == 200
    assert res.json()["id"] == created["id"]
    assert res.json()["notes"] == "g"


def test_filter_by_tag(client: TestClient):
    client.post(
        "/sneezes/",
        json={"notes": "n1", "occurred_at": _occurred_iso(), "tag_names": ["filter-me"]},
    )
    client.post(
        "/sneezes/",
        json={"notes": "n2", "occurred_at": _occurred_iso(), "tag_names": ["other"]},
    )
    res = client.get("/sneezes/me/tag/filter-me")
    assert res.status_code == 200
    body = res.json()
    assert len(body) == 1
    assert body[0]["notes"] == "n1"


def test_update_and_delete(client: TestClient):
    created = client.post(
        "/sneezes/",
        json={"notes": "old", "occurred_at": _occurred_iso(), "tag_names": ["a"]},
    ).json()
    sid = created["id"]

    upd = client.put(
        f"/sneezes/me/{sid}",
        json={
            "notes": "new",
            "occurred_at": _occurred_iso(),
            "location": "sofa",
            "volume": 7,
            "tag_names": ["b"],
        },
    )
    assert upd.status_code == 200
    assert upd.json()["notes"] == "new"
    assert {t["name"] for t in upd.json()["tags"]} == {"b"}

    del_res = client.delete(f"/sneezes/me/{sid}")
    assert del_res.status_code == 204

    assert client.get(f"/sneezes/me/{sid}").status_code == 404
