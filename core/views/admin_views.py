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


class AdminYearTutorListView(AdminTestMixin, ListView):
    """
    Generic view that lists all of the current year tutors
    in the system.
    """
    model = YearTutor


class AdminYearTutorCreateView(AdminTestMixin, CreateView):
    """
    View to create year tutor
    """
    model = YearTutor
    fields = ['tutor_year', 'year_tutor_user']

    def get_context_data(self, **kwargs):
        context = super(
            AdminYearTutorCreateView, self).get_context_data(**kwargs)
        context['form_url'] = reverse('new_tutor')
        context['form_type'] = 'Create'
        return context

    def get_success_url(self):
        return reverse('all_tutors')


class AdminYearTutorUpdateView(AdminTestMixin, UpdateView):
    model = YearTutor
    fields = ['tutor_year', 'year_tutor_user']

    def get_context_data(self, **kwargs):
        kwargs = {'pk': self.object.id}
        context = super(
            AdminYearTutorUpdateView, self).get_context_data(**kwargs)
        context['form_url'] = reverse('update_tutor', kwargs=kwargs)
        context['form_type'] = 'Update'
        return context

    def form_valid(self, form):
        tutor = self.object.year_tutor_user
        User.objects.filter(id=tutor.id).update(is_year_tutor=True)
        return super(AdminYearTutorUpdateView, self).form_valid(form)

    def get_success_url(self):
        return reverse('all_tutors')
