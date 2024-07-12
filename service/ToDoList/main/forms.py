from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserChangeForm

class EditProfileForm(UserChangeForm):
    current_password = forms.CharField(widget=forms.PasswordInput(), required=True, label="현재 비밀번호")
    new_password = forms.CharField(widget=forms.PasswordInput(), required=False, label="새 비밀번호")
    confirm_password = forms.CharField(widget=forms.PasswordInput(), required=False, label="새 비밀번호 확인")
    
    class Meta:
        model = User
        fields = ('username', 'email', 'current_password', 'new_password', 'confirm_password')

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