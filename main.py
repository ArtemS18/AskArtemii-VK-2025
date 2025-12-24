import uvicorn
from app.core.config import config

def main():
    uvicorn.run('app.web.app:app', host=config.server.host, port=config.server.port, workers=config.server.max_workers, reload=config.server.reload)

if __name__ == "__main__":
    main()