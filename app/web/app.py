import logging
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.core.config import config
from app.web.lifespan import lifespan
from app.web.logger import setup_logger
from app.web.routers import setup_routers


app = FastAPI(lifespan=lifespan, docs_url="/docs")


def setup_app() -> FastAPI:
    setup_logger(logging.INFO)
    app.mount("/static", StaticFiles(directory="static"), name="static")
    setup_routers(app)
    
    return app