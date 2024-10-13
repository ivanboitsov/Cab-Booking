import uuid

from pydantic import UUID4
from sqlalchemy import Column, Integer, String, TIMESTAMP, func
from sqlalchemy.orm import relationship

from src.db.database import Base

class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True, nullable=False)
    name = Column(String, nullable=False)
    tel = Column(String, nullable=False)
    email = Column(String, nullable=False, index=True)
    password = Column(String, nullable=False)
    user_date_auth = Column(TIMESTAMP, server_default=func.now())

    orders = relationship("Order", back_populates="user")

class CRL(Base):
    __tablename__ = "crl"

    id = Column(UUID4(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False)
    token = Column(String, index=True, nullable=False)