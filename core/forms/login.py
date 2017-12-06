from django import forms
from django.forms.widgets import TextInput, PasswordInput
from core.models import User


class LoginForm(forms.Form):
    """
    Form that is used to represent the login form.
    """
    u_attrs = {'class': 'form-control', 'placeholder': 'Username'}
    username = forms.CharField(max_length=100, widget=TextInput(attrs=u_attrs))

    pword_attrd = {'class': 'form-control', 'placeholder': 'Password'}
    password = forms.CharField(widget=PasswordInput(attrs=pword_attrd))

    class Meta:
        model = User
        fields = ('username', 'password')
