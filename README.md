# 📸 Conversational Memory Bot – AI-Powered Photo Gallery Assistant

## 📝 Overview
Conversational Memory Bot is an AI-powered chatbot designed to revolutionize the way users interact with their personal photo galleries. By integrating advanced Natural Language Processing (NLP) and AI-driven visual recognition, this system enables users to query, retrieve, and explore their photos using natural language and visual features.

---

## ✨ Features
### 1️⃣ Natural Language Querying
- Users can search their photo gallery with natural language queries like:
  - "Show me wedding images from my gallery."

### 2️⃣ Contextual Image Retrieval
- Retrieves relevant photos based on the contextual understanding of queries, matching both text and image features.

### 3️⃣ Detailed Image Descriptions
- Automatically generates textual descriptions of images, such as "This image shows a beach during sunset with two people walking."

### 4️⃣ Visual Similarity Search
- Finds images similar to a selected one based on color, objects, and scene similarity.

### 5️⃣ Automatic Tagging
- AI tags photos with keywords like "plant," "cellphone," or "handbag" for easier searching and organization.

### 6️⃣ Relevance Ranking
- Retrieved images are ranked based on how closely they match the user’s query.

### 7️⃣ Interactive Gallery
- A user-friendly interface to browse, search, and interact with uploaded images.

---


## 🛠  Technology Stack
### 🔙 Backend:
- **FastAPI** - For building the RESTful API.
- **ChromaDB** - Vector database for storing image embeddings, descriptions, metadata(image height, image width, timestamp, image_format, color_palette etc.)
- **CLIP** - Used for text and image embeddings and similarity search.
- **Gemini API (2.0 Flash)** - For generating image descriptions.

### 🎨 Frontend:
- **HTML** - Used to structure the content on the web page
- **CSS** - Used to style and design the layout of the web pages
- **JavaScript** - To add interactivity and dynamic functionality to the web pages
- **JQuery** - A JavaScript library that simplifies DOM manipulation, event handling, and AJAX interactions
  
### 🤖 AI Models:
- **Vision-based LLM/SLM** - For understanding and processing visual data.
- **Multimodal Models** - For processing combined text and image inputs using late fusion.
- **Retrieval-Augmented Generation (RAG)** - For generating responses based on retrieved image data.

---

## 🔄 System Workflow
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

## 📂 Project Structure

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

## 🚀 Getting Started

## Installation & Setup
### 📌 Prerequisites
To run this project following are need to be installed :
- Python 3.11
- FastAPI
- ChromaDB
- CLIP
- Gemini API access
  
---

## 🔑 To create a Gemini API Key
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
⚠️ **Important:** Keep your API key private and never share it publicly.

### 5. Store the API Key in .env file
- In your project root, open the .env file and add:
```bash
GOOGLE_API_KEY=your_gemini_api_key_here
```
### 6. Save the file
- Ensure .env is listed in .gitignore so the key isn’t uploaded to version control.

---

## ⚙ Installation Steps:
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

## 🔗 **API Endpoints**
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

## 📸 ScreenShots 

<img width="1366" height="647" alt="home1" src="https://github.com/user-attachments/assets/dcc815e6-05dc-4b6d-b827-2c3f40130563" />


**Figue 1 : This displays the homepage of Conversational Memory Bot**


<img width="1366" height="640" alt="upload" src="https://github.com/user-attachments/assets/e0736475-e3fe-4b94-86e9-2564b1a6234f" />


**Figure  2 : User can upload single or batch upload images** 


<img width="1366" height="646" alt="uploading" src="https://github.com/user-attachments/assets/be8dd8e9-b5e0-4111-908d-32a9f1d9c9a2" />


**Figure  3 : Uploading images and storing metadata, description in ChromaDB**


<img width="1366" height="631" alt="uploaded" src="https://github.com/user-attachments/assets/0d79efa6-528d-42a5-8422-8e805b102074" />


**Figure  4 : After successful uploading images**


![gall](https://github.com/user-attachments/assets/e88e1600-7caf-4386-a6d0-5b090dc60d2f)


**Figure  5 : Displays the uploaded images in gallery page**


<img width="1366" height="637" alt="view" src="https://github.com/user-attachments/assets/4acd90fa-ef12-4371-9b28-18220a2eb5a1" />


**Figure  6 : Displays the image information in view page**


<img width="1366" height="640" alt="viewall" src="https://github.com/user-attachments/assets/000ee011-fa65-4d2f-8fa2-ac63721c7e77" />


**Figure  7 : Zoom in, zoom out of images and automatic tagging**


![WhatsApp Image 2025-08-11 at 11 34 00 PM](https://github.com/user-attachments/assets/b7fd93a0-10a5-4fda-933c-b135a36778c8)


**Figure  8 : Displays retrieved images for user text query**


<img width="1366" height="651" alt="im" src="https://github.com/user-attachments/assets/77c6a9c4-9f07-4910-be69-917d471dc604" />



**Figure  9 : User query for visual similarity search**


<img width="1366" height="651" alt="imres" src="https://github.com/user-attachments/assets/9cfeee98-8cbc-4916-84e3-893ba57b5587" />


**Figure  10 : Displays retrieved images for user text query**


<img width="1366" height="644" alt="both" src="https://github.com/user-attachments/assets/79b5b211-046d-440c-bee0-4020868ec45c" />


**Figure  11 : User query for both text and images**


<img width="1366" height="643" alt="bothres" src="https://github.com/user-attachments/assets/2ffc2ed4-91bf-4766-87e1-6ddc19d0576f" />


**Figure  12 : Displays retrieved images for user text and image query**

---

## 🎯 Usage
- Upload images via the batch uploader.
- Query the chatbot using natural language or images.
- Retrieve, search, and explore personal as well as photo gallery effortlessly.

---

## 📜 License
This project is licensed under the MIT License.
