from django.urls import reverse
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView
from django.shortcuts import render

from core.views.mixins import AdminTestMixin
from core.forms import UserPermissionsForm, UserCreationForm
from core.models import User, ProgrammeTutor


class AdminYearTutorListView(AdminTestMixin, ListView):
    """
    Generic view that lists all of the current year tutors
    in the system.
    """
    model = ProgrammeTutor


class AdminYearTutorCreateView(AdminTestMixin, CreateView):
    """
    View to create year tutor
    """
    model = ProgrammeTutor
    fields = ['programme_name', 'tutor_year', 'programme_tutor_user']

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
    model = ProgrammeTutor
    fields = ['programme_name', 'tutor_year', 'programme_tutor_user']

    def get_form(self, *args, **kwargs):
        form = super(AdminYearTutorUpdateView, self).get_form(*args, **kwargs)
        # limit drop down to only contain those with year tutor permission
        form.fields['programme_tutor_user'].queryset = User.objects.filter(
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
