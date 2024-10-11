from sqlalchemy import Column, Integer, String, ForeignKey, TIMESTAMP, func
from sqlalchemy.orm import relationship

from src.database import Base

class Order(Base):
    __tablename__ = "order"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True, nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'), index=True, nullable=False)
    driver_id = Column(Integer, ForeignKey('driver.id'), index=True, nullable=False)
    order_date = Column(TIMESTAMP, server_default=func.now(), index=True, nullable=False)
    house_from_id = Column(Integer, index=True, nullable=False)
    house_from = Column(String, index=True, nullable=False)
    house_to_id = Column(Integer, index=True, nullable=False)
    house_to = Column(String, index=True, nullable=False)

    user = relationship("User", back_populates="orders")
    driver = relationship("Driver", back_populates="orders")