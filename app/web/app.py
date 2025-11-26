import logging
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.web.lifespan import lifespan
from app.web.logger import setup_logger
from app.web.routers import setup_routers

app = FastAPI(lifespan=lifespan)
app.mount("/static", StaticFiles(directory="static"), name="static")

def setup_app() -> FastAPI:
    setup_logger(logging.INFO)
    setup_routers(app)
    
    return app