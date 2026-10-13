from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import or_
from sqlalchemy.orm import Session

from app.database import get_database
from app.models import Notes, User
from app.routes.auth import get_current_user
from app.schemas import NoteCreate, NoteUpdate

router = APIRouter()


@router.post("/notes")
def create_note(
    note_data: NoteCreate,
    current_user: User = Depends(get_current_user),
    database_session: Session = Depends(get_database),
):
    new_note = Notes(
        user_id=current_user.user_id,
        title=note_data.title,
        content=note_data.content,
    )

    database_session.add(new_note)
    database_session.commit()
    database_session.refresh(new_note)

    return {
        "message": "Note Created Successfully",
        "note_id": new_note.note_id,
        "title": new_note.title,
        "content": new_note.content,
    }


@router.get("/notes")
def get_my_notes(
    search: str | None = None,
    page: int = Query(default=1, ge=1),
    limit: int = Query(default=5, ge=1, le=100),
    current_user: User = Depends(get_current_user),
    database_session: Session = Depends(get_database),
):
    skip = (page - 1) * limit

    query = database_session.query(Notes).filter(
        Notes.user_id == current_user.user_id,
        Notes.archived == False,
    )

    if search:
        query = query.filter(
            or_(
                Notes.title.contains(search),
                Notes.content.contains(search),
            )
        )

    query = query.order_by(
        Notes.pinned.desc(),
        Notes.note_id.desc(),
    )

    results = query.offset(skip).limit(limit + 1).all()

    has_next = len(results) > limit
    notes = results[:limit]

    return {
        "items": notes,
        "page": page,
        "limit": limit,
        "has_next": has_next,
    }


@router.get("/notes/{note_id}")
def get_specific_note(
    note_id: int,
    database_session: Session = Depends(get_database),
    current_user: User = Depends(get_current_user),
):
    note = (
        database_session.query(Notes)
        .filter(
            Notes.user_id == current_user.user_id,
            Notes.note_id == note_id,
        )
        .first()
    )

    if note is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Note not found",
        )

    return note


@router.put("/update_notes/{note_id}")
def update_notes(
    updated_data: NoteUpdate,
    note_id: int,
    current_user: User = Depends(get_current_user),
    database_session: Session = Depends(get_database),
):
    note = (
        database_session.query(Notes)
        .filter(
            Notes.note_id == note_id,
            Notes.user_id == current_user.user_id,
        )
        .first()
    )

    if note is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Note not found",
        )

    note.title = updated_data.title
    note.content = updated_data.content
    note.updated_at = datetime.now(timezone.utc)

    database_session.commit()
    database_session.refresh(note)

    return {
        "message": "Note updated successfully",
        "note_id": note.note_id,
        "title": note.title,
        "content": note.content,
    }


@router.delete("/notes/{note_id}")
def delete_note(
    note_id: int,
    current_user: User = Depends(get_current_user),
    database_session: Session = Depends(get_database),
):
    note = (
        database_session.query(Notes)
        .filter(
            Notes.note_id == note_id,
            Notes.user_id == current_user.user_id,
        )
        .first()
    )

    if note is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Note not found",
        )

    database_session.delete(note)
    database_session.commit()

    return {"message": "Note deleted successfully"}


@router.patch("/notes/{note_id}/pin")
def toggle_pin_note(
    note_id: int,
    current_user: User = Depends(get_current_user),
    database_session: Session = Depends(get_database),
):
    note = (
        database_session.query(Notes)
        .filter(
            Notes.note_id == note_id,
            Notes.user_id == current_user.user_id,
        )
        .first()
    )

    if note is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Note not found",
        )

    note.pinned = not note.pinned

    database_session.commit()
    database_session.refresh(note)

    return {
        "message": "Pin status updated",
        "note_id": note.note_id,
        "pinned": note.pinned,
    }


@router.patch("/notes/{note_id}/archive")
def archive(
    note_id: int,
    current_user: User = Depends(get_current_user),
    database_session: Session = Depends(get_database),
):
    note = (
        database_session.query(Notes)
        .filter(
            Notes.note_id == note_id,
            Notes.user_id == current_user.user_id,
        )
        .first()
    )

    if note is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Note not found",
        )

    note.archived = not note.archived

    database_session.commit()
    database_session.refresh(note)

    return {
        "message": "archive status updated",
        "note_id": note.note_id,
        "archived": note.archived,
    }


@router.get("/archived_notes")
def get_archived_notes(
    page: int = Query(default=1, ge=1),
    limit: int = Query(default=5, ge=1, le=100),
    current_user: User = Depends(get_current_user),
    database_session: Session = Depends(get_database),
):
    skip = (page - 1) * limit

    notes = (
        database_session.query(Notes)
        .filter(
            Notes.user_id == current_user.user_id,
            Notes.archived == True,
        )
        .order_by(
            Notes.pinned.desc(),
            Notes.note_id.desc(),
        )
        .offset(skip)
        .limit(limit)
        .all()
    )

    return notes


@router.get("/recently_updated")
def recently_updated(
    limit: int = Query(default=5, ge=1, le=100),
    current_user: User = Depends(get_current_user),
    database_session: Session = Depends(get_database),
):
    notes = (
        database_session.query(Notes)
        .filter(
            Notes.user_id == current_user.user_id,
            Notes.archived == False,
        )
        .order_by(Notes.updated_at.desc())
        .limit(limit)
        .all()
    )

    return notes