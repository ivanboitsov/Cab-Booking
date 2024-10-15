from typing import Optional

from pydantic import BaseModel, Field

class HouseSchema(BaseModel):
    id: int = Field(..., description="ID дома")
    street: str = Field(..., description="Улица")
    building: Optional[str] = Field(..., description="Строение")
    number: str = Field(..., description="Номер дома")