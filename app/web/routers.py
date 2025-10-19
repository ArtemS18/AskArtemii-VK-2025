from fastapi import FastAPI
from app.routers.routers import router
from app.routers.questions import router as question_router
from app.routers.users import router as users_router

def setup_routers(app: FastAPI):
    app.include_router(router)
    app.include_router(question_router)
    app.include_router(users_router)