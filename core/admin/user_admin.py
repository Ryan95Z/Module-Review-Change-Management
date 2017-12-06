from django import forms
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from core.models import User


class UserCreationForm(forms.ModelForm):
    """
    Form for creating new users.
    """
    # provide two fields to check passwords match
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(
        label='Password confirmation',
        widget=forms.PasswordInput
    )

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')

    def clean_password(self):
        """
        Method that will clean and validate the
        two passwords.
        """
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        """
        Method to save the user based on information
        in the form.
        """
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    """
    Form for updating the users password
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ('email', 'password', 'first_name', 'last_name', 'is_admin')

    def clean_password(self):
        """
        Method that returns the clean password
        """
        return self.initial["password"]


class UserAdmin(BaseUserAdmin):
    """
    Class that contains configuration for how
    the User model is displayed in django
    genertated admin panel.
    """
    form = UserChangeForm
    add_form = UserCreationForm

    # how users are displayed on list
    list_display = ('username', 'get_full_name', 'email')

    # filters for list
    list_filter = ('is_admin', 'is_module_leader',
                   'is_office_admin', 'is_year_tutor')

    # how fields will be displayed on form
    fieldsets = (
        (None, {'fields': ('username',)}),
        ('Personal Information', {
            'fields': ('first_name', 'last_name', 'email')}),
        ('Permissions', {
            'fields': ('is_admin', 'is_module_leader', 'is_office_admin',
                       'is_year_tutor')})
    )

    search_fields = ('username', 'email', 'first_name', 'last_name')
    ordering = ('username',)
    filter_horizontal = ()
