import os
import uvicorn

from fastapi import FastAPI
from config.database import engine
from starlette.middleware.sessions import SessionMiddleware
from routes.user_routes import router as user_router
from config.config import Config
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates


app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="views")
templates.env.globals['PROJECT'] = Config.PROJECT  # Now PROJECT is available in all templates
# Include Routes
app.add_middleware(
    SessionMiddleware,
    secret_key=Config.SECRET_KEY
)


app.include_router(user_router)

@app.get("/")
def home():
    return {"message": "Voice Assistant is running"}

# Optional: handle Chrome DevTools requests to avoid 404 logs
@app.get("/.well-known/appspecific/com.chrome.devtools.json")
def chrome_devtools_config():
    return {}

# @app.get("/")
# def home():
#     return {"message": "MySQL Connected Successfully 🚀"}

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)