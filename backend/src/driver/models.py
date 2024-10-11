from sqlalchemy import Column, Integer, String, Enum
from sqlalchemy.orm import relationship

from src.database import Base
import enum

class DriverClassEnum(enum.Enum):
    econom = "econom"
    comfortable = "comfortable"
    business = "business"

class Driver(Base):
    __tablename__ = "driver"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True,nullable=False)
    name = Column(String, nullable=False)
    tel = Column(String, nullable=False)
    car = Column(String, nullable=False)
    driver_class = Column(Enum(DriverClassEnum), nullable=False)

    orders = relationship("Order", back_populates="driver")