from fastapi import Form
from pydantic import BaseModel, root_validator, EmailStr
import bcrypt
import uuid
from datetime import datetime


class UserInput(BaseModel):
    username: str = Form(...)
    password: str = Form(...)
    email: EmailStr = Form(...)

    @root_validator(pre=True)
    def hash_password(cls, values):
        if 'password' in values:
            hashed_password = bcrypt.hashpw(
                values['password'].encode('utf-8'), bcrypt.gensalt())
            values['password'] = hashed_password.decode('utf-8')
        return values


class UserOutput(BaseModel):
    user_id: uuid.UUID
    username: str
    created_at: datetime

    class Config:
        orm_mode = True


class UserLogin(BaseModel):
    username: str = Form(...)
    password: str = Form(...)

    @root_validator(pre=True)
    def hash_password(cls, values):
        if 'password' in values:
            hashed_password = bcrypt.hashpw(
                values['password'].encode('utf-8'), bcrypt.gensalt())
            values['password'] = hashed_password.decode('utf-8')
        return values
