from django.urls import reverse
from django.views.generic import View
from django.views.generic.list import ListView
from django.views.generic.edit import UpdateView
from django.shortcuts import redirect, get_object_or_404

from timeline.models import TimelineEntry
from timeline.utils.changes import process_changes, revert_changes
from django.http import HttpResponse


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


class TimelinePostViews(View):
    """
    Base View for making post requests to the
    timeline.
    """
    def get(self, request, *args, **kwargs):
        """
        Get method to return user to the timeline,
        if they attempt to access the view.
        """
        return redirect(redirect(self._get_url(**kwargs)))

    def _get_url(self, **kwargs):
        """
        Method to get the url once finished processing.
        """
        kwargs.pop('pk', '')
        return reverse('module_timeline', kwargs=kwargs)


class TimelineUpdateStatus(TimelinePostViews):
    """
    View to enable a timeline entry to be updated,
    which will push the changes in the model it is monitoring.
    """

    def post(self, request, *args, **kwargs):
        """
        Post method to take the current entry and
        move it to the next status. If confirmed from
        being at status 'Staged', it will make the changes
        to the model.
        """
        entry_pk = kwargs['pk']
        module_pk = kwargs['module_pk']

        # get the current timeline entry.
        entry = get_object_or_404(TimelineEntry, pk=entry_pk)

        if entry.status == 'Draft':
            entry.status = 'Staged'
        elif entry.status == 'Staged':
            process_changes(entry_pk)
            entry.status = 'Confirmed'
        else:
            pass
        entry.save()
        return redirect(self._get_url(**kwargs))


class TimelineRevertStage(TimelinePostViews):
    """
    View to allow uncommited changes to be pushed
    back to the previous status before confirmed.
    Once it is a draft, it will have changes deleted
    with the entry.
    """
    def post(self, request, *args, **kwargs):
        """
        Post request to enable the rollback
        """
        entry_pk = kwargs['pk']
        module_pk = kwargs['module_pk']

        entry = get_object_or_404(TimelineEntry, pk=entry_pk)
        if entry.status == 'Draft':
            revert_changes(entry_pk)
            entry.delete()
        elif entry.status == 'Staged':
            entry.status = 'Draft'
            entry.save()
        else:
            pass
        return redirect(self._get_url(**kwargs))
