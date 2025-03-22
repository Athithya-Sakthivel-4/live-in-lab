from fastapi import FastAPI, File, UploadFile, HTTPException, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import sqlite3
import os
import uuid
import logging
from pathlib import Path
from models.face_recognition import extract_face_embedding, verify_faces

# Initialize FastAPI app
app = FastAPI()

# Configure Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Ensure directories exist
BASE_DIR = Path(__file__).parent
STATIC_DIR = BASE_DIR / "static"
UPLOAD_FOLDER = STATIC_DIR / "uploads"
TEMPLATES_DIR = BASE_DIR / "templates"

STATIC_DIR.mkdir(exist_ok=True)
UPLOAD_FOLDER.mkdir(parents=True, exist_ok=True)

# ✅ Fix: Ensure Static Files are Mounted Before Template Usage
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

# Set up Jinja2 templates
templates = Jinja2Templates(directory=TEMPLATES_DIR)

# Database path
DB_PATH = BASE_DIR / "children.db"

# Allowed image formats
ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png"}

# ✅ Fix: Ensure Static Paths Are Correctly Referenced in Jinja2
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})
