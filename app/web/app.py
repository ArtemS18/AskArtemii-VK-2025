from fastapi import FastAPI

from app.web.logger import setup_logger
from app.web.routers import setup_routers

app = FastAPI()

def setup_app() -> FastAPI:
    setup_logger()
    setup_routers(app)
    return app