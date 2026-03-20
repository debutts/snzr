from domains.tag.models import Tag
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

def repo_get_tag_by_names(names: list[str]) -> Tag | None:
  with Session(engine) as session:
    statement = select(Tag).where(Tag.name in names)
    tags = list(session.exec(statement).all())
    return tags

def repo_get_tag(id: str) -> Tag:
  with Session(engine) as session:
    tag = session.get(Tag, id)
    if not tag:
      raise ValueError(f"Tag with id {id} not found")
    return tag

def get_or_create_tags_by_names(session: Session, names: list[str] | None) -> list[Tag]:
    if not names:
        return []
    names = [name.strip().lower() for name in names]
    tags = repo_get_tag_by_names(names)
    tags_dict = {tag.name: tag for tag in tags}
    for name in names:
      if name not in tags_dict:
        tag = Tag(name=name)
        session.add(tag)
        session.flush()
        tags_dict[name] = tag
    return list(tags_dict.values())

def repo_delete_tag(id: str):
  with Session(engine) as session:
    tag = session.get(tag, id)
    if not tag:
      raise ValueError(f"Tag with id {id} not found")
    session.delete(tag)
    session.commit()