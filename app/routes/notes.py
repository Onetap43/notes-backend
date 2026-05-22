from fastapi import APIRouter,Depends,HTTPException,status
from sqlalchemy.orm import Session
from sqlalchemy import or_
from app.database import get_database
from app.models import Notes,User
from app.schemas import NoteCreate,NoteUpdate
from app.routes.auth import get_current_user
router=APIRouter()
@router.post("/notes")
def create_note(note_data:NoteCreate,current_user:User=Depends(get_current_user),database_session:Session=Depends(get_database)):
    new_note=Notes(user_id=current_user.user_id,title=note_data.title,content=note_data.content)
    database_session.add(new_note)
    database_session.commit()
    #note_id was created automatically but before commit it was unknown to new_note because remember new_note was same as Note class of models and you declared all attributes like user_id and title and all but note_id is created right now so remember to refresh
    database_session.refresh(new_note)
    return{"message":"Note Created Successfully","note_id": new_note.note_id,"title":new_note.title,"content":new_note.content}
@router.get("/notes")
def get_my_notes(search:str | None=None,page:int=1,limit:int=5,current_user:User=Depends(get_current_user),database_session:Session=Depends(get_database)):
    skip=(page-1)*limit
    query=database_session.query(Notes).filter(Notes.user_id==current_user.user_id)
    if search:
        query=query.filter(or_(Notes.title.contains(search),Notes.content.contains(search)))
    query=query.order_by(Notes.pinned.desc(),Notes.note_id.desc())
    notes=query.offset(skip).limit(limit).all()
    return notes
@router.get("/notes/{note_id}")
def get_specific_note(note_id:int,database_session:Session=Depends(get_database),current_user:User=Depends(get_current_user)):
    note=database_session.query(Notes).filter(Notes.user_id==current_user.user_id,Notes.note_id==note_id).first()
    if note is  None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Note not found")
    return note
@router.put("/update_notes/{note_id}")
def update_notes(updated_data:NoteUpdate,note_id:int,current_user:User=Depends(get_current_user),database_session:Session=Depends(get_database)):
    note=database_session.query(Notes).filter(Notes.note_id==note_id,Notes.user_id==current_user.user_id).first()
    if note is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Note not found")
    note.title=updated_data.title
    note.content=updated_data.content
    database_session.commit()
    database_session.refresh(note)
    return{"message":"Note updated successfully","note_id":note.note_id,"title":note.title,"content":note.content}
@router.delete("/notes/{note_id}")
def delete_note(note_id:int,current_user:User=Depends(get_current_user),database_session:Session=Depends(get_database)):
    note=database_session.query(Notes).filter(Notes.note_id==note_id,Notes.user_id==current_user.user_id).first()
    if note is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Note not found")
    database_session.delete(note)
    database_session.commit()
    return{"message":"Note deleted successfully"}
@router.patch("/notes/{note_id}/pin")
def toggle_pin_note(note_id:int,current_user:User=Depends(get_current_user),database_session:Session=Depends(get_database)):
    note=database_session.query(Notes).filter(Notes.note_id==note_id,Notes.user_id==current_user.user_id).first()
    if note is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Note not found")
    note.pinned=not note.pinned
    database_session.commit()
    database_session.refresh(note)
    return{"message":"Pin status updated","note_id":note.note_id,"pinned":note.pinned}