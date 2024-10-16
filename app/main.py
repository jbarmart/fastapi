from typing import Optional

import uvicorn
from fastapi import FastAPI, Depends, HTTPException, APIRouter, Header
from fastapi_versioning import VersionedFastAPI
from fastapi_versioning import version
from sqlalchemy.orm import Session

from app.src.models import schemas
from app.src.services import crud
from app.src.services.database import get_db


# Dependency function to check for 'token' in headers
def verify_token(token: Optional[str] = Header(None)):
    """
    curl -X GET "http://localhost:8080/v1/get_user/1" -H "token: your-expected-token"
    """
    if token != "your-expected-token":
        raise HTTPException(status_code=403, detail="Invalid token or token missing")
    return token


router = APIRouter(prefix="/api/user",
                   tags=["user"],
                   responses={404: {"description": "Not Found"}})

app = FastAPI(title="User", dependencies=[Depends(verify_token)])


@app.get("/health")
def health_check():
    return {"status": "Healthy"}


@router.get("", response_model=schemas.UserResponse)
@version(1)
@app.get("/get_user/{user_id}")
def read_user(user_id: int, db: Session = Depends(get_db)):
    """"
curl -X GET "http://localhost:8080/v1/get_user/1"
    """
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@router.post("", status_code=201, response_model=schemas.UserCreate)
@version(1)
@app.post("/create_user")
def create_user(user: schemas.UserInput, db: Session = Depends(get_db)):
    """
curl -X POST "http://localhost:8080/v1/create_user" \
-H  "accept: application/json" \
-H  "Content-Type: application/json" \
-d "{\"user_id\":7,\"username\":\"sofia\"}"
    """
    try:
        return crud.create_user(db=db, user_id=user.user_id, username=user.username)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error occurred: {e}.")


app.include_router(router)

app = VersionedFastAPI(app, version_format='{major}', prefix_format='/v{major}')

if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=8080)
