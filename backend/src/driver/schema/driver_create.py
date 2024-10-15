from pydantic import BaseModel, Field

from src.driver.enum.DriverClassEnum import DriverClassEnum

class DriverCreateSchema(BaseModel):
    name: str = Field(..., description="Имя водителя")
    tel: str = Field(..., description="Телефон водителя")
    car: str = Field(..., description="Машина водителя")
    driver_class: DriverClassEnum = Field(..., description="Класс водителя")