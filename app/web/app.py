import logging
import time
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.core.config import config
from app.lib.log import log_call
from app.web.lifespan import lifespan
from app.web.logger import setup_logger
from app.web.routers import setup_routers
from fastapi.middleware.cors import CORSMiddleware


_app = FastAPI(lifespan=lifespan, docs_url="/docs")


def setup_app() -> FastAPI:
    setup_logger(logging.INFO)
    # app.mount("/static", StaticFiles(directory="static"), name="static")
    # app.mount("/media", StaticFiles(directory="media"), name="static")
    setup_routers(_app)
    _app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:8080"], 
        allow_headers=["*"], 
        allow_methods=["DELETE", "GET", "HEAD", "OPTIONS", "PATCH", "POST", "PUT"],
        allow_credentials=True,
    )
    
    return _app

__app = setup_app()

async def app(scope, receive, send):
    log = logging.getLogger(__name__)
    log.debug("New Request %s", scope)
    start_time = time.perf_counter()
    await __app(scope, receive, send)
    end_time = time.perf_counter() - start_time
    log.info("Responsed to %.03f ms", end_time*1000)
