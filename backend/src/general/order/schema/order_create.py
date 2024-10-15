from typing import Optional

from pydantic import BaseModel, Field
from src.general.driver.enum.DriverClassEnum import DriverClassEnum

class OrderCreateSchema(BaseModel):
    house_from_street: str = Field(..., description="Улица отправления")
    house_from_building: Optional[str] = Field(..., description="Строение отправления")
    house_from_number: str = Field(..., description="Номер дома отправления")
    house_to_street: str = Field(..., description="Улица прибытия")
    house_to_building: Optional[str] = Field(..., description="Строение прибытия")
    house_to_number: str = Field(..., description="Номер дома прибытия")
    driver_class: DriverClassEnum = Field(..., description="Класс водителя")