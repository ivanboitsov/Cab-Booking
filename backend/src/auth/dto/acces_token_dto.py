from pydantic import BaseModel

class AccessTokenDTO(BaseModel):
    access_token: str
    token_type: str = "Bearer"