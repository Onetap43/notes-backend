from fastapi import APIRouter,Depends
from sqlalchemy.orm import Session
from app.database import get_database
from app.models import Notes,User
from app.schemas import NoteCreate 
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
def get_my_notes(current_user:User=Depends(get_current_user),database_session:Session=Depends(get_database)):
    my_notes=database_session.query(Notes).filter(Notes.user_id==current_user.user_id).all()
    return my_notes