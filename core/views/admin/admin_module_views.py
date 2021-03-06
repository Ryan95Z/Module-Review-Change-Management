from django.urls import reverse
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView
from django.db.models import Q

from core.views.mixins import AdminTestMixin
from core.models import Module
from core.forms import SearchForm
from timeline.utils.timeline.helpers import publish_changes
from timeline.utils.notifications.helpers import (WatcherWrapper,
                                                  push_notification)


class AdminModuleListView(AdminTestMixin, ListView):
    """
    View for listing all modules
    """
    model = Module
    paginate_by = 10

    def get_queryset(self):
        """
        Returns the query set for the view. If we have a search
        then it will return items based of the seach. Otherwise,
        it will return all objects.
        """
        search = self.request.GET.get('search', "")
        if len(search) > 0:
            # search for modules by the name or code
            object_list = self.model.objects.filter(
                Q(module_name__icontains=search) |
                Q(module_code__icontains=search)
            )
            return object_list
        return super(AdminModuleListView, self).get_queryset()

    def get_context_data(self, *args, **kwargs):
        context = super(
            AdminModuleListView, self).get_context_data(*args, **kwargs)
        context['search_form'] = SearchForm
        return context


class AdminModuleCreateView(AdminTestMixin, CreateView):
    model = Module
    fields = ['module_code', 'module_name', 'module_credits', 'module_level',
              'semester', 'delivery_language', 'module_leader']

    def get_context_data(self, **kwargs):
        context = super(AdminModuleCreateView, self).get_context_data(**kwargs)
        context['form_url'] = reverse('new_module')
        context['form_type'] = 'Create'
        return context

    def get_success_url(self):
        # before sending success url, connect the user
        # to recieve notifiations
        obj = self.object
        publish_changes(obj, self.request.user)
        watcher = WatcherWrapper(obj.module_leader)

        # add the module created to thier list
        watcher.add_module(obj)

        # push notification to module leader
        push_notification(
            'module_leader',
            module_code=obj.module_code,
            module_leader=obj.module_leader
        )
        return reverse('all_modules')


class AdminModuleUpdateView(AdminTestMixin, UpdateView):
    model = Module
    fields = ['module_name', 'module_credits', 'module_level',
              'semester', 'delivery_language', 'module_leader']

    def get_context_data(self, **kwargs):
        kwargs = {'pk': self.object.module_code}
        context = super(AdminModuleUpdateView, self).get_context_data(**kwargs)
        context['form_url'] = reverse('update_module', kwargs=kwargs)
        context['form_type'] = 'Update'
        return context

    def post(self, request, *args, **kwargs):
        original_module_leader = self.get_object().module_leader
        response = super(
            AdminModuleUpdateView, self).post(request, *args, **kwargs)

        # check to see that the module leader may have changed.
        current_module_leader = self.object.module_leader
        if current_module_leader != original_module_leader:
            # create watcher objects for module leaders
            original_ml_watcher = WatcherWrapper(original_module_leader)
            current_ml_watcher = WatcherWrapper(current_module_leader)

            # update module status by removing or adding module
            original_ml_watcher.remove_module(self.object)
            current_ml_watcher.add_module(self.object)

            # push the notification to the new module leader
            push_notification(
                'module_leader',
                module_code=self.object.module_code,
                module_leader=current_module_leader
            )
        # publish changes to timeline
        publish_changes(self.object, request.user)
        return response

    def get_success_url(self):
        return reverse('all_modules')
