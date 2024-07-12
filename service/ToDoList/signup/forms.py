from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='이메일을 입력하세요.')
    role = forms.ChoiceField(choices=(('user', '일반사용자'), ('admin', '관리자')), required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'role', 'password1', 'password2')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not email:
            raise forms.ValidationError('이메일을 입력해주세요.')
        return email
