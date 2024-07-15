from ultralytics import YOLO
from pathlib import Path
import cv2
import os
from django.conf import settings

# Load YOLO model
model_path = Path(__file__).resolve().parent / 'model'
model = YOLO(model_path / "best.pt")

# Define the label to name mapping
label_to_name = {
    0: "아스팔트 도로파임",
    1: "콘크리트 도로파임",
    2: "종방향 균열",
    3: "횡방향 균열",
    4: "거북등 균열",
    5: "줄눈부 파손",
    6: "십자 파손",
    7: "절삭보수부 파손",
    8: "긴급보수부 파손",
    15: "규제봉",
    16: "맨홀",
    17: "배수로"
}


def detect_objects(image_path):
    results = model(image_path)
    detected_image = results[0].plot()  # This returns a numpy array
    result = []
    for obj in results[0].boxes:
        label = int(obj.cls.item())
        confidence = float(obj.conf.item())
        category_name = label_to_name.get(label, "Unknown")
        result.append((category_name, confidence))

    # Save the detected image to the media directory
    result_image_name = f"detected_{Path(image_path).name}"
    result_image_path = os.path.join(
        settings.MEDIA_ROOT, 'images', result_image_name)

    # Save the image (this will overwrite any existing file with the same name)
    cv2.imwrite(result_image_path, detected_image)

    return result, result_image_name
