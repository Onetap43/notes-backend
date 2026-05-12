from pydantic import BaseModel
class signupdata(BaseModel):
    username: str
    password:str
class logindata(BaseModel):
    username: str
    password: str
class TokenResponse(BaseModel):
    access_token: str
    token_type: str
class NoteCreate(BaseModel):
    title: str
    content: str
class NoteUpdate(BaseModel):
    title: str
    content: str
class NoteResponse(BaseModel):
    note_id: int
    title: str
    content: str
class Config:
    from_attributes=True