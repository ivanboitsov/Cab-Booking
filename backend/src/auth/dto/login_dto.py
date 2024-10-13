from pydantic import BaseModel, EmailStr, constr

from src.config import MIN_PASSWORD_LENGTH

class LoginDTO(BaseModel):
    email: EmailStr
    password: constr(min_length=MIN_PASSWORD_LENGTH)