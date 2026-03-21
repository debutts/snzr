from domains.sneeze.models import Sneeze, SneezeTagLink
from domains.sneeze.requests import UpdateSneezeRequest
from domains.tag.models import Tag
from infrastructure.persistence.common.db_engine import engine
from infrastructure.persistence.tag_repository import \
    repo_get_or_create_tags_by_names
from sqlmodel import Session, select


def _save_sneeze(session: Session, sneeze: Sneeze) -> Sneeze:
    session.add(sneeze)
    session.commit()
    statement = select(Sneeze).where(Sneeze.id == sneeze.id)
    loaded = session.exec(statement).first()
    if loaded is None:
        raise RuntimeError("Sneeze missing after save")
    return loaded


def repo_create_sneeze(sneeze: Sneeze, tag_names: list[str] | None = None) -> Sneeze:
    with Session(engine) as session:
        tags = repo_get_or_create_tags_by_names(session, tag_names)
        sneeze.tags = tags
        return _save_sneeze(session, sneeze)


def repo_get_sneeze_by_id(sneeze_id: str, user_id: str):
    with Session(engine) as session:
        statement = select(Sneeze).where(Sneeze.id == sneeze_id)
        sneeze = session.exec(statement).first()
        if not sneeze:
            raise ValueError(f"Sneeze with id {sneeze_id} not found")
        if sneeze.user_id != user_id:
            raise PermissionError(f"User does not have permission to read sneeze with id {sneeze_id}")
        return sneeze


def repo_get_all_sneezes_by_user_id(user_id: str) -> list[Sneeze]:
    with Session(engine) as session:
        statement = select(Sneeze).where(Sneeze.user_id == user_id).order_by(Sneeze.occurred_at.desc())
        result = session.exec(statement)
        return list(result.unique().all())

def repo_get_all_sneezes_by_tag_and_user(tag: str, user_id: str) -> list[Sneeze]:
    with Session(engine) as session:
        statement = select(Sneeze).join(SneezeTagLink).join(Tag).where(Tag.name == tag and Sneeze.user_id == user_id).order_by(Sneeze.occurred_at.desc())
        result = session.exec(statement)
        return list(result.unique().all())

def repo_update_sneeze(id: str, user_id: str, update_request: UpdateSneezeRequest) -> Sneeze:
    with Session(engine) as session:
        statement = select(Sneeze).where(Sneeze.id == id)
        sneeze = session.exec(statement).first()
        if not sneeze:
            raise ValueError(f"Sneeze with id {id} not found")
        if sneeze.user_id != user_id:
            raise PermissionError(f"User does not have permission to edit sneeze with id {id}")
        tags = repo_get_or_create_tags_by_names(session, update_request.tag_names)
        sneeze.tags = tags
        sneeze.notes = update_request.notes
        sneeze.occurred_at = update_request.occurred_at
        sneeze.location = update_request.location
        sneeze.volume = update_request.volume
        return _save_sneeze(session, sneeze)


def repo_delete_sneeze(sneeze_id: str, user_id: str) -> None:
    with Session(engine) as session:
        sneeze = session.get(Sneeze, sneeze_id)
        if not sneeze:
            raise ValueError(f"Sneeze with id {sneeze_id} not found")
        if sneeze.user_id != user_id:
            raise PermissionError(f"User does not have permission to delete sneeze with id {sneeze_id}")
        session.delete(sneeze)
        session.commit()
