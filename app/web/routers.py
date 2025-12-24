from fastapi import FastAPI
from app.handlers.autho import router
from app.handlers.grade import router as grade_rounter
from app.handlers.questions import router as question_router
from app.handlers.users import router as users_router
from app.handlers.centrifugo import router as centrifugo_router

def setup_routers(app: FastAPI):
    app.include_router(router)
    app.include_router(question_router)
    app.include_router(users_router)
    app.include_router(grade_rounter)
    app.include_router(centrifugo_router)