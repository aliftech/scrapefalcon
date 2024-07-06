from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from src.controllers.users_controller import create, get_all_users, signin
from core.config.database import get_db
from src.schemas.user_schema import UserInput, UserLogin

userRouter = APIRouter()


class UserRouters:
    @userRouter.post("/signup")
    def create(data: UserInput, session: Session = Depends(get_db)):
        signup = create(session, data)
        return signup

    @userRouter.post('/signin')
    def login(data: UserLogin, session: Session = Depends(get_db)):
        login = signin(session, data)
        return login

    @userRouter.get('/users')
    def get_all_users(skip: int = Query(0, ge=0), limit: int = Query(10, ge=1, le=100), session: Session = Depends(get_db)):
        users = get_all_users(skip, limit, session)
        return users
