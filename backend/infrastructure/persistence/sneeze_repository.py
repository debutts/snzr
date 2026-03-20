from infrastructure.persistence.common.db_engine import engine
from domains.sneeze.models import Sneeze, UpdateSneezeRequest
from sqlmodel import Session, select


def repo_create_sneeze(sneeze: Sneeze) -> Sneeze:
  with Session(engine) as session:
    session.add(sneeze)
    session.commit()
    session.refresh(sneeze)
    return sneeze

def repo_get_sneeze_by_id(sneeze_id: str, user_id: str):
  with Session(engine) as session:
    sneeze = session.get(Sneeze, sneeze_id)
    if not sneeze:
      raise ValueError(f"Sneeze with id {sneeze_id} not found")
    if sneeze.user_id != user_id:
      raise PermissionError(f"User does not have permission to read sneeze with id {id}")
    return sneeze

def repo_get_all_sneezes_by_user_id(user_id: str) -> list[Sneeze]:
  with Session(engine) as session:
    statement = select(Sneeze).where(Sneeze.user_id == user_id).order_by(Sneeze.occurred_at.desc())
    return list(session.exec(statement).all())

def repo_update_sneeze(id: str, user_id: str, update_request: UpdateSneezeRequest) -> Sneeze:
  with Session(engine) as session:
    sneeze = session.get(Sneeze, id)
    if not sneeze:
      raise ValueError(f"Sneeze with id {id} not found")
    if sneeze.user_id != user_id:
      raise PermissionError(f"User does not have permission to edit sneeze with id {id}")
    sneeze.notes = update_request.notes
    sneeze.occurred_at = update_request.occurred_at
    sneeze.location = update_request.location
    sneeze.volume = update_request.volume
    session.add(sneeze)
    session.commit()
    session.refresh(sneeze)
    return sneeze

def repo_delete_sneeze(sneeze_id: str, user_id: str) -> None:
  with Session(engine) as session:
    sneeze = session.get(Sneeze, sneeze_id)
    if not sneeze:
      raise ValueError(f"Sneeze with id {sneeze_id} not found")
    if sneeze.user_id != user_id:
      raise PermissionError(f"User does not have permission to delete sneeze with id {id}")
    session.delete(sneeze)
    session.commit()
