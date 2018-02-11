from django.urls import reverse
from django.views.generic import View
from django.views.generic.list import ListView
from django.views.generic.edit import UpdateView
from django.shortcuts import redirect

from timeline.models import TimelineEntry


class TimelineListView(ListView):
    """
    View of the timeline for the module that has
    been requested. Displays a maximum of 15 entries
    on each page.
    """
    model = TimelineEntry

    # maximum number of entries per page
    paginate_by = 15

    def get_queryset(self):
        module_id = self.kwargs['module_pk']
        return self.model.objects.filter(module=module_id)

    def get_context_data(self, *args, **kwargs):
        context = super(
            TimelineListView, self).get_context_data(*args, **kwargs)
        context['module_code'] = self.kwargs['module_pk']
        context['block_pagination'] = True
        return context


class TimelineUpdateView(UpdateView):
    """
    View to enable manual changes if user needs to
    update the entry for some reason.
    """
    model = TimelineEntry
    fields = ['changes']

    def dispatch(self, request, *args, **kwargs):
        """
        Override of dispatch method to prevent
        an entry that is not saved as a draft to be
        edited if the user attempts a manual override
        via url manipulation.
        """
        entry = self.get_object()
        kwargs = {'module_pk': entry.module_code()}

        # if status is not draft,
        # then redirect back to timeline
        if entry.status != 'Draft':
            return redirect(reverse('module_timeline', kwargs=kwargs))

        # continue with request if valid
        return super(
            TimelineUpdateView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(TimelineUpdateView, self).get_context_data(**kwargs)
        context['title'] = self.object.title
        context['pk'] = self.object.pk
        context['module_code'] = self.object.module_code()
        return context

    def get_success_url(self):
        kwargs = {'module_pk': self.object.module_code()}
        return reverse('module_timeline', kwargs=kwargs)
