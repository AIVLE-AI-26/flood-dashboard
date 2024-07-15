from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
import re

class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='이메일을 입력하세요.', required=True)
    role = forms.ChoiceField(choices=(('user', '일반사용자'), ('admin', '관리자')), required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'role', 'password1', 'password2')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not email:
            raise forms.ValidationError('이메일을 입력해주세요.')
        email_regex = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        if not re.match(email_regex, email):
            raise forms.ValidationError('유효한 이메일 주소를 입력해주세요.')
        return email

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if not username:
            raise forms.ValidationError('아이디를 입력해주세요.')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('이미 존재하는 아이디입니다.')
        if len(username) < 5:
            raise forms.ValidationError('아이디는 최소 5자 이상이어야 합니다.')
        return username

    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')
        if not password1:
            raise forms.ValidationError('비밀번호를 입력해주세요.')
        if len(password1) < 8:
            raise forms.ValidationError('비밀번호는 최소 8자 이상이어야 합니다.')
        return password1
