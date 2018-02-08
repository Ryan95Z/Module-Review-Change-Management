from django.shortcuts import render
from django.views.generic import View
from django.views.generic.list import ListView
from timeline.models import TimelineEntry


class TimelineListView(ListView):
    model = TimelineEntry

    def get_queryset(self):
        module_id = self.kwargs['module_pk']
        return self.model.objects.filter(module=module_id)

    def get_context_data(self, *args, **kwargs):
        context = super(
            TimelineListView, self).get_context_data(*args, **kwargs)
        context['module_code'] = self.kwargs['module_pk']
        return context
