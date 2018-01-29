from django.urls import reverse
from django.views import View
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView
from django.shortcuts import render

from .mixins import AdminTestMixin
from core.forms import UserPermissionsForm, UserCreationForm
from core.models import User, YearTutor, Module


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

    def get_form(self, *args, **kwargs):
        form = super(AdminYearTutorCreateView, self).get_form(*args, **kwargs)
        # limit drop down to only contain those with year tutor permission
        form.fields['year_tutor_user'].queryset = User.objects.filter(
            is_year_tutor=True)
        return form

    def get_context_data(self, **kwargs):
        context = super(
            AdminYearTutorCreateView, self).get_context_data(**kwargs)
        # url for form action
        context['form_url'] = reverse('new_tutor')
        # button text
        context['form_type'] = 'Create'
        return context

    def get_success_url(self):
        return reverse('all_tutors')


class AdminYearTutorUpdateView(AdminTestMixin, UpdateView):
    """
    View to update existing year tutor
    """
    model = YearTutor
    fields = ['tutor_year', 'year_tutor_user']

    def get_form(self, *args, **kwargs):
        form = super(AdminYearTutorUpdateView, self).get_form(*args, **kwargs)
        # limit drop down to only contain those with year tutor permission
        form.fields['year_tutor_user'].queryset = User.objects.filter(
            is_year_tutor=True)
        return form

    def get_context_data(self, **kwargs):
        kwargs = {'pk': self.object.id}
        context = super(
            AdminYearTutorUpdateView, self).get_context_data(**kwargs)
        # url for form action
        context['form_url'] = reverse('update_tutor', kwargs=kwargs)
        # button text
        context['form_type'] = 'Update'
        return context

    def get_success_url(self):
        return reverse('all_tutors')


class AdminModuleListView(AdminTestMixin, ListView):
    model = Module


class AdminModuleCreateView(AdminTestMixin, CreateView):
    model = Module
    fields = ['module_code', 'module_name', 'module_credits', 'module_level',
              'module_year', 'semester', 'delivery_language', 'module_leader']

    def get_context_data(self, **kwargs):
        context = super(AdminModuleCreateView, self).get_context_data(**kwargs)
        context['form_url'] = reverse('new_module')
        context['form_type'] = 'Create'
        return context

    def get_success_url(self):
        return reverse('all_modules')


class AdminModuleUpdateView(AdminTestMixin, UpdateView):
    model = Module
    fields = ['module_code', 'module_name', 'module_credits', 'module_level',
              'module_year', 'semester', 'delivery_language', 'module_leader']

    def get_context_data(self, **kwargs):
        kwargs = {'pk': self.object.module_code}
        context = super(AdminModuleUpdateView, self).get_context_data(**kwargs)
        context['form_url'] = reverse('update_module', kwargs=kwargs)
        context['form_type'] = 'Update'
        return context

    def get_success_url(self):
        return reverse('all_modules')
