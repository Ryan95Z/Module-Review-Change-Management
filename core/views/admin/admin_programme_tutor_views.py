from django.urls import reverse
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from core.views.mixins import AdminTestMixin
from core.models import User, Module, ProgrammeTutor

from timeline.utils.notifications.helpers import WatcherWrapper

YEAR_LEVELS = {
    'Year 1': 'L4',
    'Year 2': 'L5',
    'Year 3': 'L6',
    'MSC': 'L7',
}


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
    fields = ['programme_name', 'tutor_year', 'programme_tutor_user']

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
        return context

    def get_success_url(self):
        self.__process_watchers()
        return reverse('all_tutors')

    def __process_watchers(self):
        """
        Private method to add modules to tutor watch list
        """
        user = self.object.programme_tutor_user

        # convert module year to level
        module_level = YEAR_LEVELS[self.object.tutor_year]

        # get the modules
        modules = Module.objects.filter(module_level=module_level)

        # add the modules to user's watch list
        tutor_watcher = WatcherWrapper(user)
        tutor_watcher.bulk_module_add(*list(modules))


class AdminProgrammeTutorUpdateView(AdminTestMixin, UpdateView):
    """
    View to update existing programme tutor
    """
    model = ProgrammeTutor
    fields = ['programme_name', 'tutor_year']

    def get_context_data(self, **kwargs):
        kwargs = {'pk': self.object.id}
        context = super(
            AdminProgrammeTutorUpdateView, self).get_context_data(**kwargs)
        # url for form action
        context['form_url'] = reverse('update_tutor', kwargs=kwargs)
        # button text
        context['form_type'] = 'Update'
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
        updated_year = request.POST.get('tutor_year', None)
        obj = self.get_object()
        current_year = obj.tutor_year

        # if the years are the same, stop and
        # don't make the changes.
        if updated_year == current_year:
            return

        # since years are different, proceed with changes
        updated_modules_lvl = None

        # covert the year, if it does not match, return
        # and let django handle the error
        try:
            updated_modules_lvl = YEAR_LEVELS[updated_year]
        except KeyError:
            return

        # get the new modules for the tutor to watch
        updated_modules = list(Module.objects.filter(
            module_level=updated_modules_lvl
        ))

        # covert the year again to get the modules the
        # tutor is currently watching. These will be removed
        # As before, if the level is wrong, let django handle
        # it by returning.
        current_modules_lvl = None
        try:
            current_modules_lvl = YEAR_LEVELS[current_year]
        except KeyError:
            return

        # get the current modules
        current_modules = list(Module.objects.filter(
            module_level=current_modules_lvl
        ))

        # update watch list by removing current modules and adding new ones
        tutor_watcher = WatcherWrapper(obj.programme_tutor_user)
        tutor_watcher.bulk_module_remove(*current_modules)
        tutor_watcher.bulk_module_add(*updated_modules)


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

        # get the level current level and then use it to get modules
        module_level = YEAR_LEVELS[obj.tutor_year]
        modules = Module.objects.filter(module_level=module_level)

        # remove the modules from watch list
        watcher = WatcherWrapper(obj.programme_tutor_user)
        watcher.bulk_module_remove(*list(modules))
