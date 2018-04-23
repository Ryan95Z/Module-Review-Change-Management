from django.urls import reverse
from django.http import Http404
from django.views.generic import View
from django.views.generic.list import ListView
from django.shortcuts import redirect, get_object_or_404, render
from core.models import Module

from timeline.models import TimelineEntry
from timeline.utils.notifications.helpers import push_notification
from timeline.utils.timeline.changes import revert_changes
from timeline.utils.timeline.tracking_form import get_form_version_number

from forms.utils.tracking_form import StagedTrackingFormWrapper


class TrackingFormChanges(View):
    """
    View to access all the changes from a summary timeline entry
    """
    template_name = "timeline/timeline_tracking_changes.html"

    def get(self, request, *args, **kwargs):
        module_code = kwargs.get('module_pk')
        pk = kwargs.get('pk')

        parent = get_object_or_404(TimelineEntry, pk=pk, parent_entry=None)

        # get the child entries
        entires = TimelineEntry.objects.filter(
            module_code=module_code,
            parent_entry_id=pk
        )

        if entires.count() < 1:
            raise Http404(
                "Invalid entry that does not have any related entries."
            )

        context = {
            'module_code': module_code,
            'parent': parent,
            'entries': entires,
            'version_no': get_form_version_number(pk)
        }
        return render(request, self.template_name, context)


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
        return self.model.objects.filter(
            module_code=module_id,
            parent_entry=None
        )

    def get_context_data(self, *args, **kwargs):
        context = super(
            TimelineListView, self).get_context_data(*args, **kwargs)
        context['module_code'] = self.kwargs['module_pk']
        context['block_pagination'] = True
        return context


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
        return redirect(self._get_url(**kwargs))

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

        # get the current timeline entry.
        entry = get_object_or_404(TimelineEntry, pk=entry_pk)

        if entry.status == 'Draft':
            entry.status = 'Staged'
        elif entry.status == 'Staged':  # pragma: no cover
            entry.status = 'Confirmed'

            # update the tracking form data
            module = Module.objects.get(module_code=entry.module_code)
            form = StagedTrackingFormWrapper(module)
            form.change_to_current()
        else:
            pass
        entry.approved_by = request.user
        entry.save()
        push_notification(entry.status, entry=entry, user=request.user)
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

        entry = get_object_or_404(TimelineEntry, pk=entry_pk)
        if entry.status == 'Draft':
            # remove the changes as it is no longer needed
            revert_changes(entry)
        elif entry.status == 'Staged':
            # move the status back to 'Draft'
            entry.status = 'Draft'
            entry.save()
        else:
            pass
        return redirect(self._get_url(**kwargs))
