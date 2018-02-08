from django.urls import reverse
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView
from django.db.models import Q

from core.views.mixins import AdminTestMixin
from core.models import Module
from core.forms import SearchForm

from timeline.utils.factory import EntryFactory


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
              'module_year', 'semester', 'delivery_language', 'module_leader']

    def get_context_data(self, **kwargs):
        context = super(AdminModuleCreateView, self).get_context_data(**kwargs)
        context['form_url'] = reverse('new_module')
        context['form_type'] = 'Create'
        return context

    def form_valid(self, form):
        respone = super(AdminModuleCreateView, self).form_valid(form)
        EntryFactory.makeEntry("init", self.object)
        return respone

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

    def form_valid(self, form):
        respone = super(AdminModuleUpdateView, self).form_valid(form)
        EntryFactory.makeEntry("update", self.object)
        return respone

    def get_success_url(self):
        return reverse('all_modules')
