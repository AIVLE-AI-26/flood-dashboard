from django import forms

class TermsForm(forms.Form):
    agree = forms.BooleanField(label='I agree to the terms and conditions')