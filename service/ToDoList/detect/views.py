import os
from django.shortcuts import render, redirect
from django.conf import settings
from .forms import ImageUploadForm
from .models import UploadedImage
from .detection import detect_objects


def home(request):
    return render(request, 'detect/home.html')  # 기본 경로에 대한 뷰


def upload_image(request):
    if request.method == "POST":
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_image = form.save()
            detection_result, result_image_name = detect_objects(
                uploaded_image.image.path)
            # Generate the full URL for the original and detected images
            original_image_url = os.path.join(
                settings.MEDIA_URL, uploaded_image.image.name)
            result_image_url = os.path.join(
                settings.MEDIA_URL, result_image_name)
            return render(request, 'detect/result.html', {
                'detection_result': detection_result,
                'original_image_url': original_image_url,
                'result_image_url': result_image_url
            })
    else:
        form = ImageUploadForm()
    return render(request, 'detect/upload.html', {'form': form})
