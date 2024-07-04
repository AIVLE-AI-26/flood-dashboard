from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254, required=True, help_text='이메일을 입력하세요.')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
        
