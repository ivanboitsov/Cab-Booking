from sqlalchemy import Column, Integer, String, TIMESTAMP, func

from src.database import Base

class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True, nullable=False)
    name = Column(String, nullable=False)
    tel = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True, index=True)
    password = Column(String, nullable=False)
    user_date_auth = Column(TIMESTAMP, server_default=func.now())

class CRL(Base):
    __tablename__ = "crl"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True, nullable=False)
    token = Column(String, index=True, nullable=False)