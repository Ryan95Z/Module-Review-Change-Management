from django import forms
from django.forms.widgets import TextInput, CheckboxInput
from core.models import User


class UserForm(forms.ModelForm):
    text_attr = {'class': 'form-control'}
    checkbox_attr = {'class': 'form-check-input'}

    username = forms.CharField(max_length=100, widget=TextInput(attrs=text_attr))
    email = forms.EmailField(max_length=100, widget=TextInput(attrs=text_attr))
    first_name = forms.CharField(max_length=100, widget=TextInput(attrs=text_attr))
    last_name = forms.CharField(max_length=100, widget=TextInput(attrs=text_attr))
    is_module_leader = forms.BooleanField(required=False, widget=CheckboxInput(attrs=checkbox_attr))
    is_office_admin = forms.BooleanField(required=False, widget=CheckboxInput(attrs=checkbox_attr))
    is_year_tutor = forms.BooleanField(required=False, widget=CheckboxInput(attrs=checkbox_attr))
    is_admin = forms.BooleanField(required=False, widget=CheckboxInput(attrs=checkbox_attr))

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name',
                  'is_module_leader', 'is_office_admin', 'is_year_tutor',
                  'is_admin')
