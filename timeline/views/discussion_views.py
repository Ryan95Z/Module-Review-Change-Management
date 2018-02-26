from django.urls import reverse
from django.views.generic import View
from django.http import HttpResponse
from django.shortcuts import render, redirect

from timeline.models import TimelineEntry, Discussion
from timeline.forms import DiscussionForm


class DiscussionView(View):
    template = "timeline/timeline_discussion.html"

    def get(self, request, *args, **kwargs):
        entry_id = kwargs.get('pk')
        module_code = kwargs.get('module_pk')
        entry = TimelineEntry.objects.get(pk=entry_id)

        discussion = Discussion.objects.filter(
            entry=entry_id).get_descendants(include_self=True)

        data = {
            'entry_id': entry_id,
            'module_code': module_code,
            'discussion': discussion,
            'entry': entry,
            'form': DiscussionForm
        }
        return render(request, self.template, data)

    def __redirect_url(self, **kwargs):
        return reverse('discussion', kwargs=kwargs)

    def post(self, request, *args, **kwargs):
        comment = request.POST.get('comment', '')
        form = DiscussionForm({'comment': comment})
        if form.is_valid():
            parent_id = request.POST.get('parent', None)
            parent = Discussion.objects.get(pk=parent_id)
            module_code = kwargs['module_pk']
            entry_id = kwargs['pk']
            entry = TimelineEntry.objects.get(pk=entry_id)

            Discussion.objects.create(
                comment=form.cleaned_data['comment'],
                entry=entry,
                author=request.user,
                parent=parent,
            )
        return redirect(self.__redirect_url(**kwargs))
