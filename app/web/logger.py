import logging
from logging.handlers import RotatingFileHandler
import os
import pathlib

FORMAT = "[%(asctime)s.%(msecs)03d] %(levelname)-8s %(module)10s:%(funcName)s:%(lineno)-10d %(message)s"
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

LIB_LOGGERS = ["uvicorn.access", "fastapi","uvicorn.error" ]
BASE = pathlib.Path(__file__).parent.parent.parent
LOG_FILE = os.getenv("APP__LOG_FILE", "log/web.log")

def setup_logger():
    base_logger = logging.getLogger()
    base_logger.setLevel("DEBUG")

    default_formatter = logging.Formatter(FORMAT, DATE_FORMAT)
    p = os.path.dirname(LOG_FILE)
    os.makedirs(p, exist_ok=True)
    fileHandler = RotatingFileHandler(
        LOG_FILE, 
        maxBytes=1024*1024*5, #10 MB
        backupCount=2, 
        encoding="utf-8"
    )
    fileHandler.setFormatter(default_formatter)
    
    stdHandler = logging.StreamHandler()
    stdHandler.setFormatter(default_formatter)

    base_logger.addHandler(stdHandler)
    base_logger.addHandler(fileHandler)

    for lib_logger in LIB_LOGGERS:
        log = logging.getLogger(lib_logger)
        log.setLevel("INFO")
        log.addHandler(fileHandler)
        base_logger.info("Setup file logger to %s in %s", lib_logger, LOG_FILE)
    base_logger.info("Setup root logger")
