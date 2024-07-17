import os
from django.shortcuts import render
from django.conf import settings
from .forms import ImageUploadForm
from .models import UploadedImage
from .detection import detect_objects

def home(request):
    return render(request, 'detect/upload.html')  # 기본 경로에 대한 뷰

def upload_image(request):
    detection_result = None
    original_image_url = None
    result_image_url = None

    if request.method == "POST":
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            # Clear the directory before uploading new image
            image_directory = os.path.join(settings.MEDIA_ROOT, 'images')
            for filename in os.listdir(image_directory):
                file_path = os.path.join(image_directory, filename)
                if os.path.isfile(file_path):
                    os.unlink(file_path)

            uploaded_image = form.save()
            detection_result, result_image_name = detect_objects(uploaded_image.image.path)
            # Generate the full URL for the original and detected images
            original_image_url = os.path.join(settings.MEDIA_URL, uploaded_image.image.name)
            result_image_url = os.path.join(settings.MEDIA_URL, 'images', result_image_name)
    else:
        form = ImageUploadForm()

    return render(request, 'detect/upload.html', {
        'form': form,
        'detection_result': detection_result,
        'original_image_url': original_image_url,
        'result_image_url': result_image_url
    })
