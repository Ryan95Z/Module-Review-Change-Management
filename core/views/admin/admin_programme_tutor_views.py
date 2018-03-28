from django.urls import reverse
from django.http import Http404
from django.shortcuts import render
from django.views.generic import View
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from core.views.mixins import AdminTestMixin
from core.models import User, Module, ProgrammeTutor
from core.forms import TutorForm, YEAR_LEVELS

from timeline.utils.notifications.helpers import WatcherWrapper


class AdminProgrammeTutorListView(AdminTestMixin, ListView):
    """
    Generic view that lists all of the current programme tutors
    in the system.
    """
    model = ProgrammeTutor


class AdminProgrammeTutorCreateView(AdminTestMixin, CreateView):
    """
    View to create programme tutor
    """
    model = ProgrammeTutor
    # fields = ['programme_name', 'tutor_year', 'programme_tutor_user']
    form_class = TutorForm
    template_name = "core/programmetutor_form.html"

    def get_form(self, *args, **kwargs):
        form = super(
            AdminProgrammeTutorCreateView, self).get_form(*args, **kwargs)

        # limit drop down to only contain those with programme tutor permission
        form.fields['programme_tutor_user'].queryset = User.objects.filter(
            is_year_tutor=True)
        return form

    def get_context_data(self, **kwargs):
        context = super(
            AdminProgrammeTutorCreateView, self).get_context_data(**kwargs)
        # url for form action
        context['form_url'] = reverse('new_tutor')
        # button text
        context['form_type'] = 'Create'

        # number of fields the form should loop through
        context['form_range'] = 3
        return context

    def get_success_url(self):
        self.__process_watchers()
        return reverse('all_tutors')

    def __process_watchers(self):
        """
        Private method to add modules to tutor watch list
        """
        user = self.object.programme_tutor_user

        # get the modules
        modules = self.object.modules.all()

        # add the modules to user's watch list
        tutor_watcher = WatcherWrapper(user)
        tutor_watcher.bulk_module_add(*list(modules))


class AdminProgrammeTutorUpdateView(AdminTestMixin, UpdateView):
    """
    View to update existing programme tutor
    """
    model = ProgrammeTutor
    form_class = TutorForm
    template_name = "core/programmetutor_form.html"

    def get_context_data(self, **kwargs):
        kwargs = {'pk': self.object.id}
        context = super(
            AdminProgrammeTutorUpdateView, self).get_context_data(**kwargs)

        # url for form action
        context['form_url'] = reverse('update_tutor', kwargs=kwargs)
        # button text
        context['form_type'] = 'Update'

        # number of fields the form should loop through
        context['form_range'] = 2
        return context

    def get_success_url(self):
        return reverse('all_tutors')

    def post(self, request, *args, **kwargs):
        self.__process_watchers(request)
        return super(
            AdminProgrammeTutorUpdateView, self).post(request, *args, **kwargs)

    def __process_watchers(self, request):
        """
        Private method to update the tutor's watch list
        by removing and adding relevant modules
        """

        # get the list of new module codes
        module_codes = request.POST.getlist('modules', None)
        obj = self.get_object()
        watcher = WatcherWrapper(obj.programme_tutor_user)

        # get the current and new modules
        new_modules = set(Module.objects.filter(module_code__in=module_codes))
        current_modules = set(obj.modules.all())

        # determine what needs to be removed
        modules_to_remove = list(current_modules.difference(new_modules))

        # update the modules this tutor is watching
        watcher.bulk_module_remove(*modules_to_remove)
        watcher.bulk_module_add(*list(new_modules))


class AdminProgrammeTutorDeleteView(AdminTestMixin, DeleteView):
    """
    Delete view for ProgrammeTutor
    """
    model = ProgrammeTutor

    def get_success_url(self):
        return reverse('all_tutors')

    def post(self, request, *args, **kwargs):
        self.__process_watchers()
        return super(
            AdminProgrammeTutorDeleteView, self).post(request, *args, **kwargs)

    def __process_watchers(self):
        """
        Private method that removes the modules that
        are being watched by these tutor.
        """
        obj = self.get_object()

        modules = obj.modules.all()

        # remove the modules from watch list
        watcher = WatcherWrapper(obj.programme_tutor_user)
        watcher.bulk_module_remove(*list(modules))


class FormCheckboxesView(View):
    """
    Method to retrieve checkboxes for the form
    when a specific year is provided.
    """
    def post(self, request, *args, **kwargs):
        year = request.POST.get('year', None)
        if year is None:
            raise Http404("year has not been provided.")

        try:
            level = YEAR_LEVELS[year]
        except KeyError:
            raise Http404("Invalid year provided. \
                Can either be year 1, year 2, year 3 or MSC")

        modules = Module.objects.filter(module_level=level)
        context = {'modules': modules}
        return render(request, "core/misc/checkboxes.html", context)
