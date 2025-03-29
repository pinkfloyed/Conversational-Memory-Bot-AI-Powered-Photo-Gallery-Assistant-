from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pathlib import Path
import torch, clip, chromadb, os, uvicorn
import google.generativeai as genai
from dotenv import load_dotenv
from backend.chroma_service import get_collection
from backend.routes import gallery, upload, view, chat, search
from config import UPLOAD_DIR, HISTORY_DIR

# Load environment variables
load_dotenv()

# Initialize API keys and models
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=GOOGLE_API_KEY)

# Initialize CLIP model
device = "cuda" if torch.cuda.is_available() else "cpu"
clip_model, preprocess = clip.load("ViT-B/32", device=device)

# Initialize YOLO model
# yolo_model = torch.hub.load('ultralytics/yolov5', 'yolov5x', pretrained=True)

collection = get_collection()

# Create FastAPI app
app = FastAPI()

# Added CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# To ensure directories exist
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
HISTORY_DIR.mkdir(parents=True, exist_ok=True)

# Set up templates and static files
templates = Jinja2Templates(directory="templates")
app.mount("/static_files", StaticFiles(directory="templates/static_files"), name="static_files")
app.mount("/static", StaticFiles(directory="static"), name="static")

# Include routers
app.include_router(gallery.router)
app.include_router(upload.router)
app.include_router(view.router)
app.include_router(chat.router)
app.include_router(search.router)

if __name__ == '__main__':
    uvicorn.run("main:app", host="localhost", port=8000, reload=True)
