"""Pytest configuration: DATABASE_URL for imports, isolated SQLite engine for tests."""

from __future__ import annotations

import os

import pytest
from sqlmodel import SQLModel, create_engine
from sqlmodel.pool import StaticPool


def pytest_configure(config: pytest.Config) -> None:
    # db_engine is imported before tests run; must not raise ValueError
    os.environ.setdefault("DATABASE_URL", "sqlite:///:memory:")


@pytest.fixture
def test_engine():
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    SQLModel.metadata.create_all(engine)
    yield engine
    SQLModel.metadata.drop_all(engine)
    engine.dispose()


@pytest.fixture
def patch_engines(monkeypatch: pytest.MonkeyPatch, test_engine):
    """Bind app + repositories to the same per-test SQLite engine."""
    monkeypatch.setattr(
        "infrastructure.persistence.common.db_engine.engine",
        test_engine,
    )
    monkeypatch.setattr(
        "infrastructure.persistence.sneeze_repository.engine",
        test_engine,
    )
    monkeypatch.setattr(
        "infrastructure.persistence.tag_repository.engine",
        test_engine,
    )
    import main as main_module

    monkeypatch.setattr(main_module, "engine", test_engine)
    return test_engine
