from pydantic import BaseModel, EmailStr

class ProfileDTO(BaseModel):
    name: str
    tel: str
    email: EmailStr

class ProfileWithIdDTO(BaseModel):
    id: int
    name: str
    tel: str
    email: EmailStr