from django import forms

class PasswordResetRequestForm(forms.Form):
    username = forms.CharField(label="Enter your username", max_length=254)
    email = forms.EmailField(label="Enter your email address", max_length=254)

class VerifyCodeForm(forms.Form):
    code = forms.CharField(label="Enter the verification code", max_length=20)
    new_password = forms.CharField(label="Enter your new password", widget=forms.PasswordInput)