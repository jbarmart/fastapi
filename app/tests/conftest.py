# conftest.py
import token
from typing import Optional

import pytest
from fastapi import HTTPException, Header
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient

from app.main import app
from app.config import settings
from app.src.services.database import Base, get_db
from app.src.services.token import verify_token

"""
from app.config import settings

SQLALCHEMY_DATABASE_URL = settings.DATABASE_URL
engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
"""
# Create a new database session for testing
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="function")
def db():
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)

# Override the get_db dependency
@pytest.fixture(scope="function")
def client(db):
    settings.configure(FORCE_ENV_FOR_DYNACONF="testing")
    def override_get_db():
        try:
            yield db
        finally:
            db.close()
    def override_token(token: Optional[str] = Header(None)):
        if token is None or token != "test-token":
            raise HTTPException(status_code=403, detail="Test Token Invalid")
        return token
    app.dependency_overrides[get_db] = override_get_db
    app.dependency_overrides[verify_token] = override_token
    with TestClient(app) as c:
        yield c