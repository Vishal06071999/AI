import os
import uvicorn

from fastapi import FastAPI
from starlette.middleware.sessions import SessionMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from config.database import engine
from config.config import Config
from routes.user_routes import router as user_router

app = FastAPI()

# Static Files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Templates
templates = Jinja2Templates(directory="views")
templates.env.globals['PROJECT'] = Config.PROJECT

# Middleware
app.add_middleware(
    SessionMiddleware,
    secret_key=Config.SECRET_KEY
)

# Routes
app.include_router(user_router)

# Home Route
@app.get("/")
def home():
    return {"message": "Voice Assistant is running 🚀"}

# Optional Chrome DevTools Route
@app.get("/.well-known/appspecific/com.chrome.devtools.json")
def chrome_devtools_config():
    return {}

# Run Server
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    uvicorn.run(app, host="0.0.0.0", port=port)