import uvicorn
from app.config import config

def main():
    uvicorn.run('app.web.app:setup_app', host=config.HOST, port=config.PORT, workers=config.MAX_WORKERS, reload=config.RELOAD, factory=True)

if __name__ == "__main__":
    main()