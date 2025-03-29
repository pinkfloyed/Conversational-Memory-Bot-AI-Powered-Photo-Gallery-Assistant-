from fastapi import APIRouter, Form, UploadFile
from typing import Optional
import os
from config import HISTORY_DIR
from backend.store_retrieve import retrieve_similar
from backend.description_utils import generate_response ###
router = APIRouter()

@router.post("/search_combined")
async def search_combined(
        query_text: Optional[str] = Form(None),
        query_image: Optional[UploadFile] = Form(None),
        similarity_threshold: Optional[float] = Form(0.5)
):
    image_path = None
    retrieved_images = []

    # Ensure the history directory exists
    if not os.path.exists(HISTORY_DIR):
        os.makedirs(HISTORY_DIR)

    chat_responses = {
        "hi": "Hello! How may I assist you today?",
        "hello": "Greetings! How can I be of service?",
        "how are you": "I'm an AI assistant, always ready to help. How may I assist you today?",
        "who are you": "I am an AI-powered photo gallery assistant, designed to help you with image searches and descriptions.",
        "what can you do": "I can assist you with searching for images, retrieving similar images, and providing descriptions of images.",
        "tell me a joke": "I'm here to assist with professional tasks. If you need help with something specific, feel free to ask!",
        "help": "I am here to assist you with finding and managing images. Please let me know what you need.",
        "thank you": "You're welcome! If you have any further questions, don't hesitate to ask.",
        "goodbye": "Thank you for using the service. Have a great day!",
        "show me images": "Please provide a search query or upload an image, and I will find relevant images for you.",
        "describe this image": "Please upload the image you'd like to have described, and I will provide a detailed description.",
        "search images by color": "I can assist you with finding images based on specific colors. Please specify the color you're interested in.",
        "find similar images": "Please upload an image, and I will find similar images based on its content.",
        "what are image tags": "Image tags are descriptive keywords that help categorize and identify the content of an image. They assist in better searchability.",
        "how do I upload an image": "To upload an image, please use the upload button in the interface and select the file you'd like to submit.",
        "what is your name": "I am an AI assistant. You can refer to me as your image gallery assistant."
    }

    normalized_query = query_text.strip().lower() if query_text else ""

    if normalized_query in chat_responses:
        return {"response": chat_responses[normalized_query], "retrieved_images": []}
    else:
        if query_image:
            # Save the uploaded image
            image_filename = os.path.join(HISTORY_DIR, query_image.filename)
            try:
                with open(image_filename, "wb") as image_file:
                    image_file.write(await query_image.read())
                image_path = image_filename
            except Exception as e:
                return {"error": f"Failed to save image: {str(e)}"}

        if query_text and query_image:
            # Perform combined text + image search
            retrieved_images = retrieve_similar(
                query_text=query_text,
                query_image=image_path,
                w_text=0.3,
                w_image=0.7,
                similarity_threshold=similarity_threshold
            )
        elif query_text:
            # Perform text-only search
            retrieved_images = retrieve_similar(
                query_text=query_text,
                similarity_threshold=similarity_threshold
            )
        elif query_image:
            # Perform image-only search
            retrieved_images = retrieve_similar(
                query_image=image_path,
                similarity_threshold=similarity_threshold
            )
        else:
            # No input provided
            return {"error": "No query provided"}

    # Generate the response based on the retrieved images
    response = generate_response(query_text, retrieved_images)

    # Format results for frontend display
    result_images = [
        {
            "file_name": img["file_name"],
            "description": img.get("description", "No description"),
            "image_url": img["image_url"]
        }
        for img in retrieved_images
    ]

    return {"response": response, "retrieved_images": result_images}
