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
    10: "아스팔트 도로파임",
    404: "콘크리트 도로파임",
    404: "종방향 균열",
    404: "횡방향 균열",
    7: "거북등 균열",
    8: "줄눈부 파손",
    404: "십자 파손",
    404: "절삭보수부 파손",
    11: "긴급보수부 파손",
    2: "규제봉",
    3: "맨홀",
    404: "배수로"
}


def detect_objects(image_path):
    results = model(image_path)
    detected_image = results[0].plot()  # This returns a numpy array
    result = []
    for obj in results[0].boxes:
        label = int(obj.cls.item())
        confidence = float(obj.conf.item())
        if confidence >= 0.4:
            category_name = label_to_name.get(label)
            result.append((category_name, confidence))

    # Save the detected image to the media directory
    result_image_name = f"detected_{Path(image_path).name}"
    result_image_path = os.path.join(
        settings.MEDIA_ROOT, 'images', result_image_name)

    # Save the image (this will overwrite any existing file with the same name)
    cv2.imwrite(result_image_path, detected_image)

    return result, result_image_name
