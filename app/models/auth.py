from pydantic import BaseModel, EmailStr


class UserFullInfo(BaseModel):
    email: EmailStr
    phone_number: str
    first_name: str
    last_name: str
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str
