from django.urls import reverse
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView
from django.shortcuts import render

from core.views.mixins import AdminTestMixin
from core.forms import UserPermissionsForm, UserCreationForm
from core.models import User


class UserListView(AdminTestMixin, ListView):
    """
    Generic view that will list all users. Inherits
    AdminTestMixin to check that only admins can access this view.
    """
    model = User


class AdminNewUserView(AdminTestMixin, CreateView):
    model = User
    template_name_suffix = '_new_form'
    form_class = UserCreationForm

    def get_success_url(self):
        return reverse('all_users')


class AdminUpdateUserPermissions(AdminTestMixin, UpdateView):
    """
    Update view for allowing users to be updated
    """
    model = User
    template_name_suffix = '_update_form'
    form_class = UserPermissionsForm

    def get_success_url(self):
        return reverse('all_users')
