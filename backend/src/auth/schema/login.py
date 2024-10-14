from pydantic import BaseModel, EmailStr, constr, Field

from src.config import MIN_PASSWORD_LENGTH

class UserLoginSchema(BaseModel):
    email: EmailStr = Field(..., description="Электронная почта")
    password: constr(min_length=MIN_PASSWORD_LENGTH, max_length=50) = Field(..., description="Пароль, от 8 до 50 знаков")