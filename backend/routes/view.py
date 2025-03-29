from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import os, datetime, torch, clip, chromadb
from PIL import Image
from config import UPLOAD_DIR
from backend.detectobject_yolo import detect_objects
from backend.chroma_service import get_collection
from string_localisation import store_dict, view_dict

collection = get_collection()
router = APIRouter()

# Initialize templates
templates = Jinja2Templates(directory="templates")

device = "cuda" if torch.cuda.is_available() else "cpu"
clip_model, preprocess = clip.load("ViT-B/32", device=device)


@router.get("/image_view", response_class=HTMLResponse)
async def image_view(request: Request):
    # Set default values for metadata and image path
    metadata = {
        "description": view_dict["default_description"]
    }
    image_path = ""
    output_image_path = ""
    filename = view_dict["no_image_selected"]
    detected_objects = []

    return templates.TemplateResponse("image_view.html", {
        "request": request,
        "image_path": image_path,
        "output_image_path": output_image_path,
        "filename": filename,
        "metadata": metadata,
        "detected_objects": detected_objects
    })


@router.get("/image_view_page", response_class=HTMLResponse)
async def view_image(request: Request, img: str):
    # Construct the image path
    image_path = os.path.join("static", "uploads", img)

    # Check if the image exists
    if not os.path.exists(image_path):
        return HTMLResponse(status_code=404, content="Image not found")

    # Initialize default metadata
    metadata = {
        "description": "No description available.",
        "image_width": None,
        "image_height": None,
        "file_size": None,
        "image_format": None,
        "timestamp": None
    }

    try:
        # Open the image and preprocess it for the model
        image = Image.open(image_path)
        image_input = preprocess(image).unsqueeze(0).to(device)

        # Generate image embedding using CLIP
        with torch.no_grad():
            image_embedding = clip_model.encode_image(image_input).cpu().numpy().flatten().tolist()

        # Query ChromaDB for metadata using image embedding
        results = collection.query(
            query_embeddings=[image_embedding],
            n_results=1,  # Retrieve the closest match
            include=["metadatas"]
        )

        # Check if metadata is available in ChromaDB and process it
        if results.get("metadatas") and results["metadatas"]:
            metadata_result = results["metadatas"][0]

            # If metadata_result is a list containing a dictionary
            if isinstance(metadata_result, list) and len(metadata_result) > 0:
                if isinstance(metadata_result[0], dict):
                    # Extract just the dictionary
                    metadata = metadata_result[0]
            # If it's already a dictionary
            elif isinstance(metadata_result, dict):
                metadata = metadata_result
            else:
                # Handle unexpected format
                metadata = {"description": view_dict["default_description"]}
        else:
            print(view_dict["no_metadata_found"])

    except Exception as e:
        print(f"{view_dict['error_processing_image']} {e}")

    # Detect objects in the image using YOLO
    try:
        detected_objects, output_image_path = detect_objects(image_path)
    except Exception as e:
        print(f"{view_dict['error_detecting_objects']} {e}")
        detected_objects = []
        output_image_path = image_path

    # Ensure metadata is a dictionary
    if not isinstance(metadata, dict):
        metadata = {"description": str(metadata)}

    # Set default values for missing metadata fields
    metadata.setdefault("image_width", image.width)
    metadata.setdefault("image_height", image.height)
    metadata.setdefault("file_size", os.path.getsize(image_path))
    metadata.setdefault("image_format", image.format)
    metadata.setdefault("timestamp",
                        datetime.datetime.fromtimestamp(os.path.getctime(image_path)).strftime("%Y-%m-%d %H:%M:%S"))

    # Return the template with all necessary data
    return templates.TemplateResponse("image_view.html", {
        "request": request,
        "image_path": f"/static/uploads/{img}",
        "output_image_path": f"/static/outputs/{os.path.basename(output_image_path)}",
        "filename": img,
        "metadata": metadata,
        "detected_objects": detected_objects
    })
