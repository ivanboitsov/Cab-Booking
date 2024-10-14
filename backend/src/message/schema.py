from pydantic import BaseModel

class MessageSchema(BaseModel):
    description: str