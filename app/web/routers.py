from fastapi import FastAPI
from app.handlers.autho import router
from app.handlers.questions import router as question_router
from app.handlers.users import router as users_router

def setup_routers(app: FastAPI):
    app.include_router(router)
    app.include_router(question_router)
    app.include_router(users_router)