from django.urls import reverse
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.shortcuts import render

from core.views.mixins import AdminTestMixin
from core.forms import ReviewerCreationForm
from core.models import User, Reviewer, Module

from timeline.utils.notifications.helpers import WatcherWrapper


class AdminReviewerListView(AdminTestMixin, ListView):
    """
    Generic view that lists all of the current reviewers
    in the system.
    """
    model = Reviewer


class AdminReviewerCreateView(AdminTestMixin, CreateView):
    """
    View to create reviewer
    """
    model = Reviewer
    fields = ['user', 'modules']

    def get_context_data(self, **kwargs):
        context = super(AdminReviewerCreateView, self).get_context_data(**kwargs)
        context['form_url'] = reverse('new_reviewer')
        context['form_type'] = 'Create'
        return context

    def __process_watchers(self):
        # add modules that the user needs to review
        # to thier notification watch list
        user = self.object.user

        # get all the modules
        modules = list(self.object.modules.all())
        watcher = WatcherWrapper(user)
        watcher.bulk_module_add(*modules)

    def get_success_url(self):
        self.__process_watchers()
        return reverse('all_reviewers')


class AdminReviewerUpdateView(AdminTestMixin, UpdateView):
    """
    View to update existing reviewer
    """
    model = Reviewer
    fields = ['user', 'modules']

    def get_context_data(self, **kwargs):
        kwargs = {'pk': self.object.id}
        context = super(
            AdminReviewerUpdateView, self).get_context_data(**kwargs)
        # url for form action
        context['form_url'] = reverse('update_reviewer', kwargs=kwargs)
        # button text
        context['form_type'] = 'Update'
        return context

    def post(self, request, *args, **kwargs):
        self.__process_watchers(request)
        return super(
            AdminReviewerUpdateView, self).post(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('all_reviewers')

    def __process_watchers(self, request):
        """
        Private method for processing 
        """
        module_codes = request.POST.getlist('modules', None)
        obj = self.get_object()
        watcher = WatcherWrapper(obj.user)
        new_modules = set(Module.objects.filter(module_code__in=module_codes))
        old_modules = set(obj.modules.all())
        modules_to_remove = list(old_modules.difference(new_modules))
        watcher.bulk_module_remove(*modules_to_remove)
        watcher.bulk_module_add(*list(new_modules))


class AdminReviewerDeleteView(AdminTestMixin, DeleteView):
    """
    View to delete and existing reviewer
    """
    model = Reviewer

    def post(self, request, *args, **kwargs):
        # remove all modules from list that were being watched
        obj = self.get_object()
        modules = list(obj.modules.all())
        watcher = WatcherWrapper(obj.user)
        watcher.bulk_module_remove(*modules)

        return super(
            AdminReviewerDeleteView, self).post(request, *args, **kwargs)

    def get_success_url(self):
        return reverse("all_reviewers")
