from django import forms
from django.utils.safestring import mark_safe
from .models import UploadedImage

class ImageUploadForm(forms.ModelForm):
    class Meta:
        model = UploadedImage
        fields = ['image']
        labels = {
            'image': mark_safe('AI를 이용하여 파손된 시설물을 탐지해주는 페이지입니다.<br>원하는 이미지를 업로드 해주세요.'),
        }
