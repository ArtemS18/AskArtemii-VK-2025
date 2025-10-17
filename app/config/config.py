import os

BASE_APP_DIR = "app/"

TEMPLATE_PATH = BASE_APP_DIR + "templates"

HOST = os.getenv("APP__LOCALHOST","localhost")
PORT = os.getenv("APP__PORT",8080)
MAX_WORKERS = os.getenv("APP__MAX_WORKERS",1)
RELOAD = os.getenv("APP__RELOAD",True)
