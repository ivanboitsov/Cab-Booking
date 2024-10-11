from sqlalchemy import Column, Integer, String
from src.db.database import Base

class House(Base):
    __tablename__ = "house"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True, nullable=False)
    number = Column(String, nullable=False, index=True)
    building = Column(String, index=True)
    street = Column(String, nullable=False, index=True)