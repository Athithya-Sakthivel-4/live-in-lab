from fastapi import FastAPI, File, UploadFile, HTTPException, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import sqlite3
import os
import uuid
import logging
import cv2
import numpy as np
from pathlib import Path
from verify import find_match  # ✅ Import the match function

# ✅ Define Directories
BASE_DIR = Path(__file__).parent
STATIC_DIR = BASE_DIR / "static"
UPLOAD_FOLDER = STATIC_DIR / "uploads"
TEMPLATES_DIR = BASE_DIR / "templates"

# ✅ Ensure required directories exist
STATIC_DIR.mkdir(exist_ok=True)
UPLOAD_FOLDER.mkdir(parents=True, exist_ok=True)

# ✅ Initialize FastAPI app
app = FastAPI()

# ✅ Configure Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ✅ Mount Static Files
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

# ✅ Register Jinja Templates
templates = Jinja2Templates(directory=TEMPLATES_DIR)

# ✅ Database path
DB_PATH = BASE_DIR / "children.db"
ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png"}

# ✅ Home Route
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# ✅ Upload Page
@app.get("/upload", response_class=HTMLResponse)
async def upload(request: Request):
    return templates.TemplateResponse("upload.html", {"request": request})

# ✅ Database Page
@app.get("/database", response_class=HTMLResponse)
async def database(request: Request):
    return templates.TemplateResponse("database.html", {"request": request})

# ✅ About Page
@app.get("/about", response_class=HTMLResponse)
async def about(request: Request):
    return templates.TemplateResponse("about.html", {"request": request})

# ✅ Search Page
@app.get("/search", response_class=HTMLResponse)
async def search(request: Request):
    return templates.TemplateResponse("search.html", {"request": request})

# ✅ Image Upload Route
@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    # Validate file type
    file_extension = os.path.splitext(file.filename)[-1].lower()
    if file_extension not in ALLOWED_EXTENSIONS:
        raise HTTPException(status_code=400, detail="Invalid file type")

    # Generate a unique filename
    unique_filename = f"{uuid.uuid4().hex}{file_extension}"
    file_path = UPLOAD_FOLDER / unique_filename

    # Save the uploaded file
    with open(file_path, "wb") as buffer:
        buffer.write(await file.read())

    return JSONResponse({"filename": unique_filename, "message": "File uploaded successfully!"})

# ✅ API for Searching a Missing Child
@app.post("/api/search")
async def search_child(file: UploadFile = File(...)):
    file_extension = os.path.splitext(file.filename)[-1].lower()
    if file_extension not in ALLOWED_EXTENSIONS:
        raise HTTPException(status_code=400, detail="Invalid file type")

    # Save uploaded image temporarily
    temp_file = UPLOAD_FOLDER / f"search_{uuid.uuid4().hex}{file_extension}"
    with open(temp_file, "wb") as buffer:
        buffer.write(await file.read())

    # ✅ Call verify.py function
    match = find_match(str(temp_file))

    if match:
        return JSONResponse({"status": "Match Found", "child": match})
    else:
        return JSONResponse({"status": "No Match Found"})
