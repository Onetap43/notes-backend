from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from app.database import get_database
from app.models import Notes, Tag, User
from app.routes.auth import get_current_user

router = APIRouter()


class TagCreate(BaseModel):
    name: str = Field(min_length=1, max_length=40)


def find_tag(db: Session, user_id: int, tag_id: int):
    tag = db.query(Tag).filter(Tag.tag_id == tag_id, Tag.user_id == user_id).first()
    if tag is None:
        raise HTTPException(status_code=404, detail="Tag not found")
    return tag


def find_note(db: Session, user_id: int, note_id: int):
    note = db.query(Notes).filter(Notes.note_id == note_id, Notes.user_id == user_id).first()
    if note is None:
        raise HTTPException(status_code=404, detail="Note not found")
    return note


def tag_result(tag: Tag):
    return {"tag_id": tag.tag_id, "name": tag.name}


@router.post("/tags", status_code=201)
def create_tag(
    data: TagCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_database),
):
    name = data.name.strip().lower()
    if not name:
        raise HTTPException(status_code=422, detail="Tag name cannot be blank")

    existing = db.query(Tag).filter(Tag.user_id == current_user.user_id, Tag.name == name).first()
    if existing:
        raise HTTPException(status_code=409, detail="Tag already exists")

    tag = Tag(user_id=current_user.user_id, name=name)
    db.add(tag)
    db.commit()
    db.refresh(tag)
    return tag_result(tag)


@router.get("/tags")
def list_tags(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_database),
):
    tags = db.query(Tag).filter(Tag.user_id == current_user.user_id).order_by(Tag.name).all()
    return [tag_result(tag) for tag in tags]


@router.delete("/tags/{tag_id}")
def delete_tag(
    tag_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_database),
):
    tag = find_tag(db, current_user.user_id, tag_id)
    db.delete(tag)
    db.commit()
    return {"message": "Tag deleted"}


@router.put("/notes/{note_id}/tags/{tag_id}")
def attach_tag(
    note_id: int,
    tag_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_database),
):
    note = find_note(db, current_user.user_id, note_id)
    tag = find_tag(db, current_user.user_id, tag_id)
    if tag not in note.tags:
        note.tags.append(tag)
        db.commit()
    return {"note_id": note_id, "tag_id": tag_id, "message": "Tag attached"}


@router.delete("/notes/{note_id}/tags/{tag_id}")
def detach_tag(
    note_id: int,
    tag_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_database),
):
    note = find_note(db, current_user.user_id, note_id)
    tag = find_tag(db, current_user.user_id, tag_id)
    if tag in note.tags:
        note.tags.remove(tag)
        db.commit()
    return {"note_id": note_id, "tag_id": tag_id, "message": "Tag removed"}


@router.get("/notes/{note_id}/tags")
def get_note_tags(
    note_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_database),
):
    note = find_note(db, current_user.user_id, note_id)
    return [tag_result(tag) for tag in sorted(note.tags, key=lambda t: t.name)]


@router.get("/tags/{tag_id}/notes")
def get_tagged_notes(
    tag_id: int,
    page: int = Query(default=1, ge=1),
    limit: int = Query(default=5, ge=1, le=100),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_database),
):
    find_tag(db, current_user.user_id, tag_id)
    query = db.query(Notes).filter(
        Notes.user_id == current_user.user_id,
        Notes.archived.is_(False),
        Notes.tags.any(Tag.tag_id == tag_id),
    ).order_by(Notes.pinned.desc(), Notes.note_id.desc())

    results = query.offset((page - 1) * limit).limit(limit + 1).all()
    return {
        "items": results[:limit],
        "page": page,
        "limit": limit,
        "has_next": len(results) > limit,
    }
