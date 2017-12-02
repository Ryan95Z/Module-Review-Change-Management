from django import forms
from django.forms.widgets import TextInput, PasswordInput
from core.models import User

class LoginForm(forms.Form):
	username = forms.CharField(max_length=100, 
		widget=TextInput(attrs={'class' : 'form-control', 'placeholder' : 'Username'}))
	
	password = forms.CharField(widget=PasswordInput(
		attrs={'class' : 'form-control', 'placeholder' : 'Password'}))

	class Meta:
		model = User
		fields = ('username', 'password')
