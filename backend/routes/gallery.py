from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
import os
from config import UPLOAD_DIR

router = APIRouter()

templates = Jinja2Templates(directory="templates")

@router.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@router.get("/gallery", response_class=JSONResponse, tags=["Gallery"])
async def gallery():
    try:
        if not UPLOAD_DIR.exists():
            raise HTTPException(status_code=404, detail="Upload directory not found")

        images = [f"/static/uploads/{img}" for img in os.listdir(UPLOAD_DIR) if img.endswith(("png", "jpg", "jpeg"))]
        return {"images": images}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error loading gallery: {str(e)}")

@router.get("/gallery_page", response_class=HTMLResponse)
async def gallery_page(request: Request):
    images = [f"/static/uploads/{img}" for img in os.listdir(UPLOAD_DIR) if img.endswith(("png", "jpg", "jpeg"))]
    return templates.TemplateResponse("gallery.html", {"request": request, "images": images})
