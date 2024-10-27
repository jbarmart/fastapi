from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException


from app.src.models.models import User


def get_user(db: Session, user_id: int):
    return db.query(User).filter(User.user_id == user_id).first()


def create_user(db: Session, user_id: int, username: str):
    db_user = User(user_id=user_id, username=username)
    db.add(db_user)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="User already exists")
    db.refresh(db_user)
    return db_user

# python
def update_user(db: Session, user_id: int, username: str):
    db_user = db.query(User).filter(User.user_id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    db_user.username = username
    db.commit()
    db.refresh(db_user)
    return db_user