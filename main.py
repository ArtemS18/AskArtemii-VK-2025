import uvicorn
from app.web.app import setup_app
from app.config import config

def main():
    app = setup_app()
    uvicorn.run(app, config.HOST, config.PORT, workers=config.MAX_WORKERS, reload=config.RELOAD)

if __name__ == "__main__":
    main()