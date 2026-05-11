from pydantic import BaseModel, ConfigDict, Field, EmailStr



class UserCreate(BaseModel):
    username: str = Field(... , max_length=180, min_length=1)
    email: EmailStr
    password: str = Field(... , max_length=100, min_length=1)

class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr

    model_config = ConfigDict(from_attributes=True)