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


class UserDetailsForm(forms.ModelForm):
    """
    Form that is used to allow users to chanage thier personal inforamtion
    based on the User model.
    """
    attrs = {'class': 'form-control'}
    username = forms.CharField(required=True, widget=TextInput(attrs=attrs))
    first_name = forms.CharField(required=True, widget=TextInput(attrs=attrs))
    last_name = forms.CharField(required=True, widget=TextInput(attrs=attrs))
    email = forms.EmailField(required=True, widget=TextInput(attrs=attrs))

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')
