from fastapi import FastAPI

from src.routes.user_router import userRouter

app = FastAPI()

app.include_router(userRouter)


@app.get('/')
def root_api():
    return {"message": "Welcome to ScrapeFalcon API"}
