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


class UserPasswordForm(forms.Form):
    """
    Form that is used to change the user's password. Creates two password
    input fields to compare if the passwords are the same.
    """
    attrs = {'class': 'form-control'}
    password1 = forms.CharField(label="Password", required=True,
                                widget=forms.PasswordInput(attrs=attrs))

    password2 = forms.CharField(label="Confirm Password", required=True,
                                widget=forms.PasswordInput(attrs=attrs))

    def clean_password(self):
        """
        Method that will check and clean the user's password.
        If they do not match then raises forms.ValidationError.
        """
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def update_password(self, user_id):
        """
        Method that will update the user's password.

        @param user_id  int
        @return         boolean
        """
        user = User.objects.get(id=user_id)
        if user is None:
            return False
        try:
            password = self.clean_password()
        except forms.ValidationError:
            return False
        user.set_password(password)
        user.save()
        return True
