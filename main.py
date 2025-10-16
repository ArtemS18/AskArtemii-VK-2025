import uvicorn
from app.web.app import setup_app

def main():
    app = setup_app()
    uvicorn.run(app=app)

if __name__ == "__main__":
    main()