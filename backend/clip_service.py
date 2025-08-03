import torch
import clip
from PIL import Image
import numpy as np

device = "cuda" if torch.cuda.is_available() else "cpu"
clip_model, preprocess = clip.load("ViT-B/32", device=device)

def encode_image(image_path):
    image = preprocess(Image.open(image_path).convert("RGB")).unsqueeze(0).to(device)
    with torch.no_grad():
        image_embedding = clip_model.encode_image(image).cpu().numpy().flatten().tolist()
    return image_embedding

def encode_text(text):
    text_tokens = clip.tokenize(text).to(device)
    with torch.no_grad():
        text_embedding = clip_model.encode_text(text_tokens).detach().cpu().numpy().flatten()
    return text_embedding

def combine_embeddings(text_embedding, image_embedding, w_text=0.3, w_image=0.7):
    text_embedding = text_embedding / np.linalg.norm(text_embedding)
    image_embedding = np.array(image_embedding) / np.linalg.norm(image_embedding)

    combined = w_text * text_embedding + w_image * image_embedding
    combined = combined / np.linalg.norm(combined)

    return combined
