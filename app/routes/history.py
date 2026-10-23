from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.database import get_database
from app.models import NoteVersion, Notes, User
from app.routes.auth import get_current_user

router = APIRouter()


def get_owned_note(db: Session, user_id: int, note_id: int) -> Notes:
    note = db.query(Notes).filter(
        Notes.note_id == note_id,
        Notes.user_id == user_id,
    ).first()
    if note is None:
        raise HTTPException(status_code=404, detail="Note not found")
    return note


def version_data(version: NoteVersion):
    return {
        "version_id": version.version_id,
        "note_id": version.note_id,
        "title": version.title,
        "content": version.content,
        "created_at": version.created_at,
    }


@router.get("/notes/{note_id}/history")
def get_history(
    note_id: int,
    limit: int = Query(default=50, ge=1, le=100),
    user: User = Depends(get_current_user),
    db: Session = Depends(get_database),
):
    get_owned_note(db, user.user_id, note_id)
    versions = db.query(NoteVersion).filter(
        NoteVersion.note_id == note_id,
    ).order_by(NoteVersion.version_id.desc()).limit(limit).all()
    return [version_data(version) for version in versions]


@router.post("/notes/{note_id}/history/{version_id}/restore")
def restore_version(
    note_id: int,
    version_id: int,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_database),
):
    note = get_owned_note(db, user.user_id, note_id)
    version = db.query(NoteVersion).filter(
        NoteVersion.note_id == note_id,
        NoteVersion.version_id == version_id,
    ).first()
    if version is None:
        raise HTTPException(status_code=404, detail="Version not found")

    # Keep the current state as a new snapshot so restoring is reversible.
    if note.title != version.title or note.content != version.content:
        db.add(NoteVersion(
            note_id=note.note_id,
            title=note.title,
            content=note.content,
        ))
        note.title = version.title
        note.content = version.content
        note.updated_at = datetime.now(timezone.utc)
        db.commit()
        db.refresh(note)

    return {
        "message": "Version restored",
        "note_id": note.note_id,
        "title": note.title,
        "content": note.content,
    }
