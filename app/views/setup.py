from fastapi import FastAPI
from app.views.autho import router as autho_router
from app.views.questions import router as question_router
from app.views.users import router as users_router


def setup_routers(app: FastAPI):
    app.include_router(autho_router)
    app.include_router(question_router)
    app.include_router(users_router)    