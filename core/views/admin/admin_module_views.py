from django.urls import reverse
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView
from django.shortcuts import render

from core.views.mixins import AdminTestMixin
from core.models import Module


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
