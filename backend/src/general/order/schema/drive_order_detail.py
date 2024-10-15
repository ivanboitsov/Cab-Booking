from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field
from src.general.driver.enum.DriverClassEnum import DriverClassEnum

class DriverOrderDetailSchema(BaseModel):
    id: int = Field(..., description="ID заказа")
    user_id: int = Field(..., description="ID пользователя")
    driver_class: DriverClassEnum = Field(..., description="Класс водителя")
    car: str = Field(..., description="Тип машины")
    house_from_id: int = Field(..., description="ID места отправления")
    house_from_street: str = Field(..., description="Улица отправления")
    house_from_building: Optional[str] = Field(..., description="Строение отправления")
    house_from_number: str = Field(..., description="Номер дома отправления")
    house_to_id: int = Field(..., description="ID места прибытия")
    house_to_street: str = Field(..., description="Улица прибытия")
    house_to_building: Optional[str] = Field(..., description="Строение прибытия")
    house_to_number: str = Field(..., description="Номер дома прибытия")
    order_time: datetime = Field(..., description="Время заказа")