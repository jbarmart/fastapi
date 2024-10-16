from pydantic import BaseModel, ConfigDict


# A Pydantic model class for FastAPI routes
class UserResponse(BaseModel):
    user_id: int
    username: str
    model_config = ConfigDict(from_attributes=True)


class UserCreate(BaseModel):
    user_id: int
    username: str
    model_config = ConfigDict(from_attributes=True)


class UserInput(BaseModel):
    user_id: int
    username: str
    model_config = ConfigDict(from_attributes=True)
