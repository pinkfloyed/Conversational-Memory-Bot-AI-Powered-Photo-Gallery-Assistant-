from fastapi import APIRouter, UploadFile, File, HTTPException, Request
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
import shutil
from pathlib import Path
import os
from config import UPLOAD_DIR
from backend.store_retrieve import store_image
from string_localisation import store_dict

router = APIRouter()


templates = Jinja2Templates(directory="templates")

@router.post("/batch_upload", tags=["Upload"])
async def upload_images(files: list[UploadFile] = File(...)):
    """Handles multiple file uploads."""
    uploaded_file_paths = []
    try:
        for file in files:
            file_path = UPLOAD_DIR / file.filename
            with open(file_path, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)
            uploaded_file_paths.append(f"/static/uploads/{file.filename}")
            store_image(file_path)
        return JSONResponse(content={
            "success": True,
            "message": "Images uploaded successfully!",
            "file_paths": uploaded_file_paths
        })
    except Exception as e:
        raise HTTPException(status_code=500, detail=store_dict["error_uploading"].format(error=str(e)))


@router.get("/batch_upload_page", response_class=HTMLResponse, tags=["Frontend"])
async def batch_upload_page(request: Request):
    return templates.TemplateResponse("batch_upload.html", {"request": request})
