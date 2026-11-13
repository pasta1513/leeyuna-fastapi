from pydantic import BaseModel, EmailStr, ConfigDict, Field

class UserCreate(BaseModel):
    userid: str = Field(min_length=2, max_length=20, pattern=r'^[a-zA-Z0-9]+$') #영문자와 숫자로만 구성
    password: str = Field(min_length=4, max_length=24)
    email: EmailStr
    name: str = Field(min_length=2, max_length=50)

class UserResponse(BaseModel):
    userid: str
    password: str
    email: EmailStr
    name: str

    model_config = ConfigDict(from_attributes=True)