from fastapi import FastAPI

from app.web.routers import setup_routers

app = FastAPI()

def setup_app() -> FastAPI:
    setup_routers(app)
    return app