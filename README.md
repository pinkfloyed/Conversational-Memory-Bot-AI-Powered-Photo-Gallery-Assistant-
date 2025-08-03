# Conversational Memory Bot – AI-Powered Photo Gallery Assistant

## Overview
Conversational Memory Bot is an AI-powered chatbot designed to revolutionize the way users interact with their personal photo galleries. By integrating advanced Natural Language Processing (NLP) and AI-driven visual recognition, this system enables users to query, retrieve, and explore their photos using natural language and visual features.

---

## Features
### 1. Natural Language Querying
- Users can search their photo gallery with natural language queries like:
  - "Show me wedding images from my gallery."

### 2. Contextual Image Retrieval
- Retrieves relevant photos based on the contextual understanding of queries, matching both text and image features.

### 3. Detailed Image Descriptions
- Automatically generates textual descriptions of images, such as "This image shows a beach during sunset with two people walking."

### 4. Visual Similarity Search
- Finds images similar to a selected one based on color, objects, and scene similarity.

### 5. Automatic Tagging
- AI tags photos with keywords like "plant," "cellphone," or "handbag" for easier searching and organization.

### 6. Relevance Ranking
- Retrieved images are ranked based on how closely they match the user’s query.

### 7. Interactive Gallery
- A user-friendly interface to browse, search, and interact with uploaded images.

---


## Technology Stack
### Backend:
- **FastAPI** - For building the RESTful API.
- **ChromaDB** - Vector database for storing image embeddings, descriptions, metadata(image height, image width, timestamp, image_format, color_palette etc.)
- **CLIP** - Used for text and image embeddings and similarity search.
- **Gemini API (2.0 Flash)** - For generating image descriptions.

### Frontend:
- **HTML** - Used to structure the content on the web page
- **CSS** - Used to style and design the layout of the web pages
- **JavaScript** - To add interactivity and dynamic functionality to the web pages
- **JQuery** - A JavaScript library that simplifies DOM manipulation, event handling, and AJAX interactions
  
### AI Models:
- **Vision-based LLM/SLM** - For understanding and processing visual data.
- **Multimodal Models** - For processing combined text and image inputs using late fusion.
- **Retrieval-Augmented Generation (RAG)** - For generating responses based on retrieved image data.

---

## System Workflow
1. **Query Processing**
   - User inputs a text query or an image query.
   - NLP module interprets the query and generates embeddings.
2. **Image Retrieval**
   - Extract image embeddings from stored gallery images.
   - Match text embeddings or image embeddings or both with image embeddings, metadata stored in ChromaDB using similarity scoring.
3. **RAG Pipeline**
   - Retrieve top-ranked images using semantic search.
   - Generate contextual responses based on the combination of user query and retrieved images.
4. **Output Display**
   - Results are shown in an interactive gallery with llm response, images with captions.

---

## Project Structure

```text
Conversational_memory_Bot_Final_Project/
│── .venv/  # Virtual environment (hidden)
│── backend/
│   │── routes/
│   │   │── __init__.py
│   │   │── chat.py
│   │   │── gallery.py
│   │   │── search.py
│   │   │── upload.py
│   │   │── view.py
│   │── __init__.py
│   │── chroma_service.py
│   │── clip_service.py
│   │── description_utils.py
│   │── detectobject_yolo.py
│   │── image_utils.py
│   │── models.py
│   │── store_retrieve.py
│── chromadb_dir/  # ChromaDB storage
│── data/ 
│   │── dataset/ (image dataset)
│── static/
│   │── history/ (in chat application, uploaded images saved here)
│   │── outputs/ (detected objects output image saved here)
│   │── uploads/ (uploaded images saved here)
│── templates/
│   │── static_files/
│   │   │── logo.jpg
│   │   │── in.png
│   │   │── style.css
│   │── batch_upload.html
│   │── chat.html
│   │── gallery.html
│   │── image_view.html
│   │── index.html
│── .env  # environment variable for Gemini API key
│── config.py  # Configuration settings
│── main.py  # FastAPI entry point
│── requirements.txt  # Dependencies
│── yolov5x.pt  # YOLOv5 model weights
│── string_localisation.py  # Constant string file
```

---

## Getting Started

## Installation & Setup
### Prerequisites
To run this project following are need to be installed :
- Python 3.11
- FastAPI
- ChromaDB
- CLIP
- Gemini API access
  
---

## To create a Gemini API Key
To use the Gemini API for generating image descriptions, you need to create an API key from Google AI Studio.
### 1. Visit Google AI Studio API Key Page
Go to https://aistudio.google.com/app/apikey.

### 2. Sign in with your Google Account
Use the Google account you want to associate with the API usage.

### 3. Click "Create API key"
- If prompted, select a project or create a new one.
- Then click "Create API key".

### 4. Copy the Generated API Key
- After creation, your new API key will be shown on the screen.
- Click Copy to copy it to your clipboard.
- Important: Keep your API key private and never share it publicly.

### 5. Store the API Key in .env file
- In your project root, open the .env file and add:
```bash
GOOGLE_API_KEY=your_gemini_api_key_here
```
### 6. Save the file
- Ensure .env is listed in .gitignore so the key isn’t uploaded to version control.

---

## Installation Steps:
1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd project-root

2. Set up a virtual environment :
   ```bash
   python3 -m venv .venv

3. Activate the virtual environment :
   ```bash
   .venv\Scripts\activate

4. Install dependencies:
   ```bash
   pip install -r requirements.txt

5. Set up your Gemini API key in the .env file :
   GOOGLE_API_KEY=your_gemini_api_key

6. Run the FastAPI application :
   Once the dependencies are installed, run the FastAPI server locally
   ```bash
   uvicorn main:app --host localhost --port 8000 --reload

---

## **API Endpoints**
### 1. Home Page
- **URL** : `/`
- **Method** : `GET`
- **Purpose** : Displays the home page.
- **Response** : Renders the index.html template.

### 2. Gallery  
- **URL** : /gallery
- **Method** : GET
- **Purpose** : Returns a JSON response with a list of uploaded images in the gallery.
- **Response** : Returns the list of image paths in JSON format.

### 3. Gallery Page
- **URL**: /gallery_page
- **Method**: GET
- **Purpose**: Displays the gallery page with images.
- **Response**: Renders the gallery.html template, listing all images from the UPLOAD_DIR.

### 4. Image View
- **URL**: `/image_view`
- **Method**: `GET`
- **Purpose**: Renders the image view page with default metadata and placeholders for an image.
- **Response**: Returns the `image_view.html` template with placeholders for image data like path, description, and detected objects.

### 5. View Image
- **URL**: `/image_view_page`
- **Method**: `GET`
- **Purpose**: Displays a specific image with its metadata, detected objects, and processed image description.
- **Response**: Returns the image view page with metadata, object detection results, and description.

### 6. Batch Upload
- **URL**: `/batch_upload`
- **Method**: `POST`
- **Purpose**: Handles multiple image file uploads at once.
- **Response**: Returns a JSON response with a success message and paths to the uploaded files.

### 7. Batch Upload Page
- **URL**: `/batch_upload_page`
- **Method**: `GET`
- **Purpose**: Displays the batch upload page.
- **Response**: Renders the `batch_upload.html` template.

### 8. Search Combined
- **URL**: `/search_combined`
- **Method**: `POST`
- **Purpose**: Handles combined text and image queries for searching similar images.
- **Response**: Returns a JSON response with the AI-generated response and a list of retrieved images.

---

## Usage
- Upload images via the batch uploader.
- Query the chatbot using natural language or images.
- Retrieve, search, and explore personal as well as photo gallery effortlessly.

---

## License
This project is licensed under the MIT License.
