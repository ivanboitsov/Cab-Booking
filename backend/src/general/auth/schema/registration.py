from pydantic import BaseModel, Field, EmailStr, constr, field_validator, ValidationError
import re

from src.config import MIN_PASSWORD_LENGTH

class UserRegistrationSchema(BaseModel):
    name: str = Field(..., description="Полное имя пользователя")
    tel: str = Field(..., description="Номер телефона в международном формате, начинающийся с '+'")
    email: EmailStr = Field(..., description="Электронная почта")
    password: constr(min_length=MIN_PASSWORD_LENGTH, max_length=50) = Field(..., description="Пароль, от 8 до 50 знаков")

try:
    UserRegistrationSchema()
except ValidationError as exc:
    print(repr(exc.errors()[0]['type']))

@field_validator("tel")
@classmethod
def validate_phone_number(cls, value: str) -> str:
    pattern = r'^\+7 \(\d{3}\) \d{3} \d{2}-\d{2}$'
    if not re.match(pattern, value):
        raise ValueError('Номер телефона должен быть в формате "+7 (xxx) xxx xx-xx"')
    return value