from ultralytics import YOLO
from pathlib import Path
import cv2
import os
from django.conf import settings

# Load YOLO model
model_path = Path(__file__).resolve().parent / 'model'
model = YOLO(model_path / "best.pt")


def detect_objects(image_path):
    results = model(image_path)
    detected_image = results[0].plot()  # This returns a numpy array
    result = []
    for obj in results[0].boxes:
        label = int(obj.cls.item())
        confidence = float(obj.conf.item())
        result.append((label, confidence))

    # Save the detected image to the media directory
    result_image_name = f"detected_{Path(image_path).name}"
    result_image_path = os.path.join(
        settings.MEDIA_ROOT, 'images', result_image_name)

    # Save the image (this will overwrite any existing file with the same name)
    cv2.imwrite(result_image_path, detected_image)

    return result, result_image_name