from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, MetaData, Table, select
from app.src.models.models import Base
from fastapi import Depends

# Fix the typo in the database name to match the reference in create_all()
engine = create_engine("sqlite:///users.db")
#
metadata = MetaData()
#
Base.metadata.create_all(bind=engine)
#
users = Table('users', metadata, autoload_with=engine)


def get_db():
    db = sessionmaker(autocommit=False, autoflush=False, bind=engine)()
    try:
        yield db
    finally:
        db.close()
