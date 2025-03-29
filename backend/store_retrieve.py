from backend.chroma_service import get_collection
from backend.clip_service import encode_image, encode_text, combine_embeddings
from backend.image_utils import extract_colors, categorize_image, extract_metadata
from backend.description_utils import generate_caption, generate_response
import numpy as np, json, os
from string_localisation import store_dict

# Initialize database collection
collection = get_collection()


def store_image(image_path):
    try:
        image_path = os.path.normpath(image_path)  # Normalize path format
        image_embedding = encode_image(image_path)  # Generate embeddings
        description = generate_caption(image_path) # Generate AI description
        metadata = extract_metadata(image_path) # Extract metadata
        colors = extract_colors(image_path)  # Extract dominant colors
        metadata["color_palette"] = json.dumps(colors)

        # Categorize image
        category = categorize_image(description)
        metadata["content_type"] = category
        metadata["description"] = description

        # Store data in ChromaDB
        collection.add(
            documents=[description],
            metadatas=[metadata],
            ids=[image_path.replace("\\", "/")],
            embeddings=[image_embedding]
        )
        print(f"✅ {store_dict['image_store'].format(image_path=image_path)}", flush=True)
        return {"success": True, "message": store_dict["image_store"].format(image_path=image_path)}

    except Exception as e:
        print(f"❌ {store_dict['error_storing'].format(image_path=image_path, error=e)}", flush=True)
        return {"success": False, "error": str(e)}


def retrieve_similar(query_text=None, query_image=None, w_text=0.3, w_image=0.7, similarity_threshold=0.2):
    query_embedding = None

    if query_text and query_image:
        # Process both text and image inputs
        text_embedding = encode_text(query_text)
        image_embedding = encode_image(query_image)
        query_embedding = combine_embeddings(text_embedding, image_embedding, w_text, w_image)

    elif query_text:
        query_embedding = encode_text(query_text)   # Only text query

    elif query_image:
        query_embedding = encode_image(query_image)  # Only image query

    if query_embedding is None:
        return []

    print(store_dict["retrieve_similar_images"], flush=True)

    # Perform the search using the query embedding
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=30,
        include=["metadatas", "distances"]  # Include both metadata and distances
    )

    retrieved_images = []
    metadatas = results.get("metadatas", [])
    distances = results.get("distances", [[]])  # Get distance scores

    # Find min and max distances
    if distances[0]:
        min_distance = min(distances[0])
        max_distance = max(distances[0])

        # Normalize distances to 0-1 range
        normalized_distances = [(d - min_distance) / (max_distance - min_distance) if max_distance > min_distance else 0
                                for d in distances[0]]

        if metadatas and len(metadatas) > 0 and len(distances) > 0:
            similarity_scores = [1 - d for d in normalized_distances]

            for i, (img_metadata, similarity) in enumerate(zip(metadatas[0], similarity_scores)):
                # Only include results that meet the threshold
                if similarity >= similarity_threshold:
                    file_name = img_metadata.get("file_name", "unknown.jpg")
                    image_url = f"/static/uploads/{file_name}"
                    description = img_metadata.get("description", "No description available")
                    content_type = img_metadata.get("content_type", "Unknown")

                    # Append the result with image metadata and similarity score
                    retrieved_images.append({
                        "file_name": file_name,
                        "description": description,
                        "image_url": image_url,
                        "content_type": content_type,
                        "similarity_score": round(similarity, 3)
                    })

    return retrieved_images
