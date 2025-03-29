import os, cv2, torch, sys
from string_localisation import detect_dict

yolo_model = torch.hub.load('ultralytics/yolov5', 'yolov5x', pretrained=True)

def detect_objects(image_path: str):
    img_cv = cv2.imread(image_path)

    if img_cv is None:
        return {"error": detect_dict["image_not"]}, image_path
        #return {"error": "Image not found or cannot be read."}, image_path

    # Convert the image to RGB (YOLO expects RGB images)
    img_rgb = cv2.cvtColor(img_cv, cv2.COLOR_BGR2RGB)

    # Perform inference with YOLO
    results = yolo_model(img_rgb, size=1280)

    # Convert results to Pandas DataFrame
    detections = results.pandas().xyxy[0]

    # Draw bounding boxes on the image
    for _, row in detections.iterrows():
        # Coordinates of the bounding box (x1, y1, x2, y2)
        x1, y1, x2, y2 = int(row['xmin']), int(row['ymin']), int(row['xmax']), int(row['ymax'])

        # Get label and confidence
        label = row['name']
        confidence = round(row['confidence'], 2)

        # Draw rectangle (bounding box) on the image
        cv2.rectangle(img_cv, (x1, y1), (x2, y2), (255, 0, 0), 2)  # Red box

        # Add label and confidence text on the bounding box
        cv2.putText(img_cv, f"{label} {confidence}", (x1, y1 - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 0, 0), 2, cv2.LINE_AA)

    # Save or show the image with bounding boxes
    output_image_path = image_path.replace("uploads", "outputs")
    os.makedirs(os.path.dirname(output_image_path), exist_ok=True)
    cv2.imwrite(output_image_path, img_cv)

    # Return bounding boxes and object details
    detected_objects = []
    for _, row in detections.iterrows():
        detected_objects.append({
            "label": row["name"],  # Object name
            "confidence": round(row["confidence"], 2)  # Rounded confidence score
        })

    return detected_objects, output_image_path
