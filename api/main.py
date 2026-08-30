
from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from api.routes import router


# =========================
# Paths
# =========================

BASE_DIR = Path(__file__).resolve().parent.parent

TEMPLATES_DIR = BASE_DIR / "templates"
STATIC_DIR = BASE_DIR / "static"


# =========================
# FastAPI
# =========================

app = FastAPI(
    title="Employee Health Assistant",
    description="سامانه تحلیل وضعیت کاری کارکنان",
    version="1.0.0",
)


# =========================
# Static Files
# =========================

app.mount(
    "/static",
    StaticFiles(directory=STATIC_DIR),
    name="static",
)


# =========================
# Templates
# =========================

templates = Jinja2Templates(
    directory=TEMPLATES_DIR,
)


# =========================
# API Routes
# =========================

app.include_router(router)


# =========================
# Home Page
# =========================

@app.get(
    "/",
    response_class=HTMLResponse,
)
async def home(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="index.html",
    )
