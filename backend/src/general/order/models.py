from sqlalchemy import Column, Integer, String, TIMESTAMP, func, Enum
from src.general.driver.enum.DriverClassEnum import DriverClassEnum

from src.database import Base


class Order(Base):
    __tablename__ = "order"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True, nullable=False)
    user_id = Column(Integer, index=True, nullable=False)
    driver_id = Column(Integer, index=True, nullable=False)
    house_from_id = Column(Integer, index=True, nullable=False)
    house_from_street = Column(String, index=True, nullable=False)
    house_from_building = Column(String, index=True)
    house_from_number = Column(String, index=True, nullable=False)
    house_to_id = Column(Integer, index=True, nullable=False)
    house_to_street = Column(String, index=True, nullable=False)
    house_to_building = Column(String, index=True)
    house_to_number = Column(String, index=True, nullable=False)
    driver_class = Column(Enum(DriverClassEnum), index=True, nullable=False)
    car = Column(String, index=True, nullable=False)
    order_date = Column(TIMESTAMP, server_default=func.now(), index=True, nullable=False)