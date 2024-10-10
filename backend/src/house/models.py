from sqlalchemy import Column, Integer, String, TIMESTAMP, ForeignKey, JSON
from src.database import  Base

class House(Base):
    __tablename__ = "house"

    id = Column(Integer, primary_key=True, index=True)
    number = Column(String, nullable=False, index=True)
    building = Column(String, index=True)
    street = Column(String, nullable=False, index=True)