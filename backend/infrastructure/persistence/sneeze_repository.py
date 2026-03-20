from domains.sneeze.models import Sneeze
from domains.sneeze.requests import UpdateSneezeRequest
from infrastructure.persistence.common.db_engine import engine
from infrastructure.persistence.tag_repository import get_or_create_tags_by_names
from sqlmodel import Session, select


def _materialize_sneeze_tags(*sneezes: Sneeze) -> None:
    """Load tag collections while the session is open (lazy=selectin batches IN queries)."""
    for s in sneezes:
        _ = list(s.tags)


def _save_sneeze(session: Session, sneeze: Sneeze) -> Sneeze:
    session.add(sneeze)
    session.commit()
    session.refresh(sneeze)
    _materialize_sneeze_tags(sneeze)
    return sneeze


def repo_create_sneeze(sneeze: Sneeze, tag_names: list[str] | None = None) -> Sneeze:
    with Session(engine) as session:
        tags = get_or_create_tags_by_names(session, tag_names)
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
        _materialize_sneeze_tags(sneeze)
        return sneeze


def repo_get_all_sneezes_by_user_id(user_id: str) -> list[Sneeze]:
    with Session(engine) as session:
        statement = select(Sneeze).where(Sneeze.user_id == user_id).order_by(Sneeze.occurred_at.desc())
        sneezes = list(session.exec(statement).all())
        _materialize_sneeze_tags(*sneezes)
        return sneezes


def repo_update_sneeze(id: str, user_id: str, update_request: UpdateSneezeRequest) -> Sneeze:
    with Session(engine) as session:
        statement = select(Sneeze).where(Sneeze.id == id)
        sneeze = session.exec(statement).first()
        if not sneeze:
            raise ValueError(f"Sneeze with id {id} not found")
        if sneeze.user_id != user_id:
            raise PermissionError(f"User does not have permission to edit sneeze with id {id}")
        tags = get_or_create_tags_by_names(session, update_request.tag_names)
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
