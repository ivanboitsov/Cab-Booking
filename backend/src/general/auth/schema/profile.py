from pydantic import BaseModel, Field, EmailStr, field_validator
import re

class UserProfileSchema(BaseModel):
    id: int = Field(..., description="ID пользователя")
    name: str = Field(..., description="Полное имя пользователя")
    tel: str = Field(..., description="Номер телефона в международном формате, начинающийся с '+'")
    email: EmailStr = Field(..., description="Электронная почта")

    @field_validator("tel")
    @classmethod
    def validate_phone_number(cls, value: str) -> str:
        pattern = r'^\+7 \(\d{3}\) \d{3} \d{2}-\d{2}$'
        if not re.match(pattern, value):
            raise ValueError('Номер телефона должен быть в формате "+7 (xxx) xxx xx-xx"')
        return value