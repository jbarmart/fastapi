from typing import Optional
import time
import uvicorn
from fastapi import FastAPI, Request, Depends, HTTPException, APIRouter, Response, Header
from prometheus_fastapi_instrumentator import Instrumentator
from sqlalchemy.orm import Session

from app.config import settings
from app.src.models import schemas
from app.src.services import crud
from app.src.services.database import get_db
from app.src.services.token import verify_token

app = FastAPI(
    title="User",
    docs_url="/docs",  # URL for Swagger docs
    redoc_url="/redoc",  # URL for ReDoc docs
    openapi_url="/openapi.json",  # URL for OpenAPI schema
)

router = APIRouter(
    prefix="/api/user",
    tags=["user"],
    responses={404: {"description": "Not Found"}},
    dependencies=[Depends(verify_token)],
)
app.include_router(router)

# Initialize Prometheus Instrumentator
Instrumentator().instrument(app, metric_namespace='baywatch').expose(app, endpoint="/metrics")

@app.get("/health")
def health_check():
    return settings.VALUE

@router.get("", response_model=schemas.UserResponse)
@app.get("/get_user/{user_id}")
def read_user(user_id: int, db: Session = Depends(get_db)):
    """"
curl -X GET "http://localhost:8080/get_user/1"
    """
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@router.post("", status_code=201, response_model=schemas.UserCreate)
@app.post("/create_user")
def create_user(user: schemas.UserInput, db: Session = Depends(get_db)):
    """
curl -X POST "http://localhost:8080/create_user" \
-H  "accept: application/json" \
-H  "Content-Type: application/json" \
-d "{\"user_id\":7,\"username\":\"sofia\"}"
    """
    try:
        return crud.create_user(db=db, user_id=user.user_id, username=user.username)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error occurred: {e}.")

@router.put("", status_code=201, response_model=schemas.UserResponse)
@app.put("/update_user")
def update_user(user_id: int, user: schemas.UserInput, db: Session = Depends(get_db)):
    """
curl -X 'PUT' \
  'http://0.0.0.0:8080/update_user?user_id=1' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "user_id": 1,
  "username": "update_jacob"
}'
    """
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return crud.update_user(db=db, user_id=user_id, username=user.username)

if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=8080)




