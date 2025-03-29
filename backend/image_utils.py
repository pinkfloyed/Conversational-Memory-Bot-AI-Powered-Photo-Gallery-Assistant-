import cv2, os, datetime
import numpy as np
from PIL import Image
from sklearn.cluster import KMeans


def extract_colors(image_path, num_colors=5):
    image = cv2.imread(image_path)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image = image.reshape((-1, 3))

    kmeans = KMeans(n_clusters=num_colors, n_init=10)
    kmeans.fit(image)
    colors = kmeans.cluster_centers_.astype(int)

    return colors.tolist()


def categorize_image(description):
    categories = ["Nature", "Food", "People", "Buildings", "Animals", "Abstract", "Objects"]
    for category in categories:
        if category.lower() in description.lower():
            return category
    return "Unknown"


def extract_metadata(image_path):
    image = Image.open(image_path)
    return {
        "file_name": os.path.basename(image_path),
        "image_path": image_path.replace("\\", "/"),
        "image_width": image.size[0],
        "image_height": image.size[1],
        "image_format": image.format,
        "file_size": os.path.getsize(image_path),
        "timestamp": datetime.datetime.fromtimestamp(os.path.getctime(image_path)).strftime("%Y-%m-%d %H:%M:%S"),
    }
