from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from .models import CustomUser

User = get_user_model()

class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='이메일을 입력하세요.', required=True)
    user_role = forms.ChoiceField(choices=(('user', '일반사용자'), ('admin', '관리자')), required=True)
    birth_date = forms.DateField(help_text='생년월일을 입력하세요.', required=True)
    first_name = forms.CharField(max_length=30, required=True, help_text='이름을 입력하세요.')
    last_name = forms.CharField(max_length=30, required=True, help_text='성을 입력하세요.')

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'user_role', 'password1', 'password2', 'birth_date', 'first_name', 'last_name')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not email:
            raise forms.ValidationError('이메일을 입력해주세요.')
        if User.objects.filter(email=email).exists():  # 여기서 User 대신 CustomUser를 사용
            raise forms.ValidationError('이미 등록된 이메일입니다.')
        return email

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if not username:
            raise forms.ValidationError('아이디를 입력해주세요.')
        if User.objects.filter(username=username).exists():  # 여기서 User 대신 CustomUser를 사용
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
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.birth_date = self.cleaned_data['birth_date']
        user.user_role = self.cleaned_data['user_role']
        print(f"Saving user: {user.username}, {user.email}, {user.birth_date}, {user.user_role}")
        
        if commit:
            user.save()
            print(f"User {user.username} saved successfully.")
        else:
            print(f"User {user.username} not saved (commit=False).")
        
        return user




class EditProfileForm(forms.ModelForm):
    current_password = forms.CharField(widget=forms.PasswordInput(), required=True, label="현재 비밀번호")
    new_password = forms.CharField(widget=forms.PasswordInput(), required=False, label="새 비밀번호")
    confirm_password = forms.CharField(widget=forms.PasswordInput(), required=False, label="새 비밀번호 확인") 
    class Meta:
        model = CustomUser
        fields = ['email', 'first_name', 'last_name', 'birth_date', 'user_role']
    
    def clean_current_password(self):
        current_password = self.cleaned_data.get('current_password')
        if not self.instance.check_password(current_password):
            raise forms.ValidationError("현재 비밀번호가 올바르지 않습니다.")
        return current_password

    def clean(self):
        cleaned_data = super().clean()
        new_password = cleaned_data.get("new_password")
        confirm_password = cleaned_data.get("confirm_password")

        if new_password and new_password != confirm_password:
            self.add_error('confirm_password', "새 비밀번호가 일치하지 않습니다.")
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        new_password = self.cleaned_data["new_password"]
        if new_password:
            user.set_password(new_password)
        if commit:
            user.save()
        return user