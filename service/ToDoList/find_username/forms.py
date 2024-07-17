from django import forms

class FindUsernameForm(forms.Form):
    email = forms.EmailField(label="Enter your email address", max_length=254)