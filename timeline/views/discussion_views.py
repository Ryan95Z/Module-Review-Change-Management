from markdown import markdown
from abc import ABC, abstractmethod
from django.urls import reverse
from django.views.generic import View
from django.views.generic.edit import UpdateView, DeleteView
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.utils.dateformat import format

from timeline.models import TimelineEntry, Discussion
from timeline.forms import DiscussionForm


class AjaxableResponseMixin(ABC, object):
    def dispatch(self, request, *args, **kwargs):
        if request.method.lower() == 'get' and request.is_ajax():
            handle = self.http_method_not_allowed(request, *args, **kwargs)
        elif request.method.lower() == 'post' and request.is_ajax():
            handle = self.ajax_post(request, *args, **kwargs)
        else:
            handle = super(
                AjaxableResponseMixin, self).dispatch(request, *args, **kwargs)
        return handle

    @abstractmethod
    def ajax_post(self, request, *args, **kwargs):
        pass


class DiscussionView(AjaxableResponseMixin, View):
    """
    View to get and post the active discussion
    for a entry in the timeline.
    """
    template = "timeline/timeline_discussion.html"

    def get(self, request, *args, **kwargs):
        """
        GET Method for accessing the view
        """
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

    def post(self, request, *args, **kwargs):
        """
        POST Method for adding new comments to the discussion
        """
        self.__process_new_discussion(request, *args, **kwargs)
        return redirect(self.__redirect_url(**kwargs))

    def ajax_post(self, request, *args, **kwargs):
        discussion = self.__process_new_discussion(request, *args, **kwargs)
        action_kwargs = {
            'module_pk': self.kwargs['module_pk'],
            'entry_pk': self.kwargs['pk'],
            'pk': discussion.id,
        }
        author_kwargs = {'pk': request.user.id}
        data = {
            'author': request.user.username,
            'time': 'just now',
            'id': discussion.pk,
            'md': discussion.comment,
            'content': markdown(discussion.comment),
            'timestamp': format(discussion.created, u'U'),
            'edit_url': reverse('edit_comment', kwargs=action_kwargs),
            'delete_url': reverse('delete_comment', kwargs=action_kwargs),
            'author_url': reverse('user_profile', kwargs=author_kwargs),
        }
        return JsonResponse(data)

    def __redirect_url(self, **kwargs):
        """
        Private method to get the response url
        """
        return reverse('discussion', kwargs=kwargs)

    def __process_new_discussion(self, request, *args, **kwargs):
        comment = request.POST.get('comment', '')
        form = DiscussionForm({'comment': comment})
        discussion = {}
        if form.is_valid():
            # add the author and comments
            discussion['comment'] = form.cleaned_data['comment']
            discussion['author'] = request.user

            # get the timeline entry
            entry_id = kwargs['pk']
            discussion['entry'] = TimelineEntry.objects.get(pk=entry_id)

            # get the parent if one has been provided
            parent_id = request.POST.get('parent', None)
            if parent_id is not None:
                discussion['parent'] = Discussion.objects.get(pk=parent_id)

            # create the discussion
            return Discussion.objects.create(**discussion)
        return None


class DiscussionGenericView(object):
    def get_context_data(self, *args, **kwargs):
        context = super(
            DiscussionGenericView, self).get_context_data(*args, **kwargs)
        context['module_code'] = self.kwargs['module_pk']
        context['entry_id'] = self.kwargs['entry_pk']
        context['discussion_id'] = self.kwargs['pk']
        return context

    def get_success_url(self):
        kwargs = {
            'module_pk': self.kwargs['module_pk'],
            'pk': self.kwargs['entry_pk']
        }
        return reverse('discussion', kwargs=kwargs)


class DiscussionUpdateView(DiscussionGenericView, UpdateView):
    model = Discussion
    fields = ['comment']

    def post(self, request, *args, **kwargs):
        response = super(
            DiscussionUpdateView, self).post(request, *args, **kwargs)
        if request.is_ajax():
            comment = self.get_object().comment
            data = {
                'md': comment,
                'html': markdown(comment),
            }
            return JsonResponse(data)
        return response


class DiscussionDeleteView(DiscussionGenericView, DeleteView):
    model = Discussion

    def post(self, request, *args, **kwargs):
        response = super(
            DiscussionDeleteView, self).post(request, *args, **kwargs)
        if request.is_ajax():
            return JsonResponse({'success': True})
        return response
