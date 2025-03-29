import time
from PIL import Image
import google.generativeai as genai
from dotenv import load_dotenv
import os
from string_localisation import en_dict

# Load environment variables
load_dotenv()

# Initialize Gemini
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=GOOGLE_API_KEY)
gemini_model = genai.GenerativeModel("gemini-2.0-flash")


def generate_description_with_retry(image=None, prompt=None, retries=3, delay=2):
    for attempt in range(retries):
        try:
            #print(f"⚡ Attempt {attempt + 1}: Generating response...", flush=True)
            print(en_dict["attempt"].format(attempt=attempt + 1), flush=True)
            if image:
                response = gemini_model.generate_content([prompt, image])
            else:
                response = gemini_model.generate_content([prompt])

            if response and response.text:
                return response.text.strip()

        except Exception as e:
            #print(f"⚠️ Error (Attempt {attempt + 1}): {e}", flush=True)
            print(en_dict["error_attempt"].format(attempt=attempt + 1, error=e), flush=True)
            time.sleep(delay)
            delay *= 2  # Exponential backoff

    # print("❌ Description generation failed after retries.", flush=True)
    # return "No response generated."
    print(en_dict["description_failed"], flush=True)
    return en_dict["no_response"]


def generate_caption(image_path):
    try:
        with open(image_path, "rb") as img_file:
            image = Image.open(img_file).convert("RGB")
            return generate_description_with_retry(image, "Describe this image in one sentence.")
    except Exception as e:
        print(en_dict["caption_failed"].format(error=e), flush=True)
        return "No description available."
        # print(f"⚠️ Caption generation failed: {e}", flush=True)
        # return "No description available."


def generate_response(query, retrieved_images):
    descriptions = [img["description"] for img in retrieved_images if "description" in img]
    descriptions = descriptions if descriptions else ["No relevant descriptions found."]

    if query and retrieved_images:
        prompt = (
            f"The user provided both a text query and an image.\n"
            f"Query: '{query}'\n"
            f"Based on this query, the following images were retrieved:\n{descriptions}\n"
            f"Generate a response that combines both the query and the images."
        )
    elif query:
        prompt = (
            f"The user asked: '{query}'.\n"
            f"Based on this query, the following images were retrieved:\n{descriptions}\n"
            f"Generate a response based on the text query and retrieved image descriptions."
        )
    elif retrieved_images:
        prompt = (
            f"The user uploaded an image but did not provide a text query.\n"
            f"Here are the descriptions of the retrieved images:\n{descriptions}\n"
            f"Generate a response solely based on the image descriptions."
        )
    else:
        prompt = "No query or images provided. Please provide a text query or upload an image."
    return generate_description_with_retry(prompt=prompt)
