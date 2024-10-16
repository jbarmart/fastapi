import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app, verify_token
from app.src.services.database import Base, get_db

SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

test_engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}, echo=True
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)


def override_get_db():
    Base.metadata.create_all(bind=test_engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=test_engine)


def override_verify_token():
    return "your-override-token"


app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[verify_token] = override_verify_token
client = TestClient(app)


@pytest.fixture(scope="function", autouse=True)
def setup_and_teardown_db():
    Base.metadata.create_all(bind=test_engine)
    yield
    Base.metadata.drop_all(bind=test_engine)


def test_create_user():
    payload = {"user_id": 1, "username": "jacob"}
    header = {"token": "your-expected-token"}
    response = client.post("/v1/create_user", json=payload, headers=header)
    print(response)
    assert response.status_code == 200
    #user = test_db.query(User).filter_by(user_id=1, username="jacob").first()
    #assert user is not None
    #assert user == "jacob"
    #assert user.user_id == 1
    #assert user.username == "jacob"
    #print("PASSED")
    #test_db.query(User).delete()


def test_read_user():
    header = {"token": "your-expected-token"}
    response = client.get("/v1/get_user/1", headers=header)
    assert response.status_code == 200
    assert response.json()["username"] == "jacob"
    print("PASSED")


def test_read_user_not_found():
    response = client.get("/v1/get_user/101")
    assert response.status_code == 404
    assert response.json()["detail"] == "User not found"
