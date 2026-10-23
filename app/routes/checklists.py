from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field, model_validator
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.database import get_database
from app.models import ChecklistItem, Notes, User
from app.routes.auth import get_current_user

router = APIRouter()


class ChecklistCreate(BaseModel):
    text: str = Field(min_length=1, max_length=300)


class ChecklistUpdate(BaseModel):
    text: str | None = Field(default=None, min_length=1, max_length=300)
    completed: bool | None = None

    @model_validator(mode="after")
    def require_change(self):
        if self.text is None and self.completed is None:
            raise ValueError("Provide text or completed")
        return self


def owned_note(db: Session, user_id: int, note_id: int) -> Notes:
    note = db.query(Notes).filter(
        Notes.note_id == note_id, Notes.user_id == user_id
    ).first()
    if note is None:
        raise HTTPException(status_code=404, detail="Note not found")
    return note


def owned_item(db: Session, note_id: int, item_id: int) -> ChecklistItem:
    item = db.query(ChecklistItem).filter(
        ChecklistItem.note_id == note_id, ChecklistItem.item_id == item_id
    ).first()
    if item is None:
        raise HTTPException(status_code=404, detail="Checklist item not found")
    return item


def item_response(item: ChecklistItem):
    return {
        "item_id": item.item_id,
        "note_id": item.note_id,
        "text": item.text,
        "completed": item.completed,
        "position": item.position,
    }


def mark_updated(note: Notes):
    note.updated_at = datetime.now(timezone.utc)


@router.get("/notes/{note_id}/checklist")
def list_items(
    note_id: int,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_database),
):
    owned_note(db, user.user_id, note_id)
    items = db.query(ChecklistItem).filter(
        ChecklistItem.note_id == note_id
    ).order_by(ChecklistItem.position, ChecklistItem.item_id).all()
    complete = sum(1 for item in items if item.completed)
    return {
        "items": [item_response(item) for item in items],
        "completed": complete,
        "total": len(items),
    }


@router.post("/notes/{note_id}/checklist", status_code=201)
def add_item(
    note_id: int,
    data: ChecklistCreate,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_database),
):
    note = owned_note(db, user.user_id, note_id)
    label = data.text.strip()
    if not label:
        raise HTTPException(status_code=422, detail="Checklist item cannot be blank")
    next_position = db.query(func.max(ChecklistItem.position)).filter(
        ChecklistItem.note_id == note_id
    ).scalar()
    item = ChecklistItem(
        note_id=note_id,
        text=label,
        completed=False,
        position=0 if next_position is None else next_position + 1,
    )
    db.add(item)
    mark_updated(note)
    db.commit()
    db.refresh(item)
    return item_response(item)


@router.patch("/notes/{note_id}/checklist/{item_id}")
def update_item(
    note_id: int,
    item_id: int,
    data: ChecklistUpdate,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_database),
):
    note = owned_note(db, user.user_id, note_id)
    item = owned_item(db, note_id, item_id)
    if data.text is not None:
        label = data.text.strip()
        if not label:
            raise HTTPException(status_code=422, detail="Checklist item cannot be blank")
        item.text = label
    if data.completed is not None:
        item.completed = data.completed
    mark_updated(note)
    db.commit()
    db.refresh(item)
    return item_response(item)


@router.delete("/notes/{note_id}/checklist/{item_id}")
def delete_item(
    note_id: int,
    item_id: int,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_database),
):
    note = owned_note(db, user.user_id, note_id)
    item = owned_item(db, note_id, item_id)
    db.delete(item)
    mark_updated(note)
    db.commit()
    return {"message": "Checklist item deleted"}
