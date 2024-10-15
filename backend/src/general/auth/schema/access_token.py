from pydantic import BaseModel, Field

class AccessTokenSchema(BaseModel):
    access_token: str = Field(..., description="Токен пользователя")
    token_type: str = Field(default="Bearer", description="Тип токена")