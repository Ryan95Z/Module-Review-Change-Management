from django.urls import reverse
from django.views.generic import View
from django.http import HttpResponse
from django.shortcuts import render

from timeline.models import Discussion


class DiscussionView(View):
    template = "timeline/timeline_discussion.html"

    def get(self, request, *args, **kwargs):
        entry_id = kwargs.get('pk')

        thread = Discussion.objects.filter(
            entry=entry_id).get_descendants(include_self=True)

        data = {
            'data': thread,
        }
        return render(request, self.template, data)
