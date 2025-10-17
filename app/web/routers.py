from fastapi import FastAPI
from app.routers.routers import router

def setup_routers(app: FastAPI):
    app.include_router(router)