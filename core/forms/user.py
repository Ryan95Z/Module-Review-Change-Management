from django import forms
from django.forms.widgets import TextInput, CheckboxInput
from core.models import User


class UserPermissionsForm(forms.ModelForm):
    """
    Custom user form based on the User model
    """
    # attributes
    checkbox_attr = {'class': 'form-check-input'}

    is_module_leader = forms.BooleanField(required=False, widget=CheckboxInput(
        attrs=checkbox_attr))

    is_office_admin = forms.BooleanField(required=False, widget=CheckboxInput(
        attrs=checkbox_attr))

    is_year_tutor = forms.BooleanField(required=False, widget=CheckboxInput(
        attrs=checkbox_attr))

    is_admin = forms.BooleanField(required=False, widget=CheckboxInput(
        attrs=checkbox_attr))

    class Meta:
        model = User
        fields = ('is_module_leader', 'is_office_admin', 'is_year_tutor',
                  'is_admin')


class UserForm(forms.ModelForm):
    input_attrs = {'class': 'form-control'}
    username = forms.CharField(required=True, max_length=40,
                               widget=TextInput(attrs=input_attrs))

    email = forms.CharField(required=True, max_length=255,
                            widget=TextInput(attrs=input_attrs))

    password = forms.CharField(required=True, max_length=255,
                               widget=TextInput(attrs=input_attrs))

    first_name = forms.CharField(required=True, max_length=255,
                                 widget=TextInput(attrs=input_attrs))

    last_name = forms.CharField(required=True, max_length=255,
                                widget=TextInput(attrs=input_attrs))

    class Meta:
        model = User
        fields = ('username', 'password', 'first_name', 'last_name', 'email')
