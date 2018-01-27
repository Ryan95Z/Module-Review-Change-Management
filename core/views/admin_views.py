from django.urls import reverse
from django.views import View
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView
from django.shortcuts import render

from .mixins import AdminTestMixin
from core.forms import UserPermissionsForm, UserCreationForm
from core.models import User, YearTutor


class UserListView(AdminTestMixin, ListView):
    """
    Generic view that will list all users. Inherits
    AdminTestMixin to check that only admins can access this view.
    """
    model = User

    def get_context_data(self, **kwargs):
        context = super(UserListView, self).get_context_data(**kwargs)
        return context


class AdminNewUserView(AdminTestMixin, CreateView):
    model = User
    template_name_suffix = '_new_form'
    form_class = UserCreationForm

    def get_success_url(self):
        return reverse('all_users')


class AdminUpdateUserPermissions(UpdateView):
    """
    Update view for allowing users to be updated
    """
    model = User
    template_name_suffix = '_update_form'
    form_class = UserPermissionsForm

    def get_context_data(self, **kwargs):
        context = super(
            AdminUpdateUserPermissions, self).get_context_data(**kwargs)
        return context

    def get_success_url(self):
        return reverse('all_users')


class AdminYearTutorListView(AdminTestMixin, ListView):
    """
    Generic view that lists all of the current year tutors
    in the system.
    """
    model = YearTutor

    def get_context_data(self, **kwargs):
        context = super(
            AdminYearTutorListView, self).get_context_data(**kwargs)
        return context
