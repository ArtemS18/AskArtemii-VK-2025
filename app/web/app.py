import logging
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.core.config import config
from app.web.lifespan import lifespan
from app.web.logger import setup_logger
from app.web.routers import setup_routers
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI(lifespan=lifespan, docs_url="/docs")


def setup_app() -> FastAPI:
    setup_logger(logging.INFO)
    app.mount("/static", StaticFiles(directory="static"), name="static")
    app.mount("/media", StaticFiles(directory="media"), name="static")
    setup_routers(app)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:8080"], 
        allow_headers=["*"], 
        allow_methods=["DELETE", "GET", "HEAD", "OPTIONS", "PATCH", "POST", "PUT"],
        allow_credentials=True,
    )
    
    return app