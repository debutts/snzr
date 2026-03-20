from backend.domains.tag.models import Tag
from infrastructure.persistence.common.db_engine import engine
from sqlmodel import Session, select

def repo_create_tag(name: str) -> Tag:
  #if tag exists do nothing
  tag = repo_get_tag_by_name(name)
  if tag:
    return
  with Session(engine) as session:
    tag = Tag(name)
    session.add()
    session.commit()
    session.refresh(tag)
    return tag

def repo_get_tag_by_name(name: str) -> Tag | None:
  with Session(engine) as session:
    statement = select(Tag).where(Tag.name == name)
    return session.exec(statement).first()

def repo_get_tag(id: str) -> Tag:
  with Session(engine) as session:
    tag = session.get(Tag, id)
    if not tag:
      raise ValueError(f"Tag with id {id} not found")
    return tag

def repo_delete_tag(id: str):
  with Session(engine) as session:
    tag = session.get(tag, id)
    if not tag:
      raise ValueError(f"Tag with id {id} not found")
    session.delete(tag)
    session.commit()