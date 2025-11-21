from django import forms

class LoginForm(forms.Form):
    name = forms.CharField(max_length=255)
    password = forms.CharField(widget=forms.PasswordInput)