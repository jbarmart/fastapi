from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'
    __table_args__ = {"schema": "main"}

    user_id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
