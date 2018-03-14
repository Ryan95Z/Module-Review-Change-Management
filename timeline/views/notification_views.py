from timeline.models import Notification
from django.views.generic import View
from django.views.generic.list import ListView
from django.shortcuts import redirect, get_object_or_404
from django.http import JsonResponse


class UnseenNotificationView(ListView):
    model = Notification

    def get_queryset(self):
        username = self.kwargs['username']
        return self.model.objects.get_unseen_notifications(username)


class NotificationRedirectView(View):
    model = Notification

    def get(self, request, *args, **kwargs):
        notification_id = kwargs['pk']
        notification = get_object_or_404(self.model, pk=notification_id)
        notification.seen = True
        notification.save()
        return redirect(notification.link)


class GetNotifications(View):
    model = Notification

    def dispatch(self, request, *args, **kwargs):
        if request.method.lower() == 'post' or request.is_ajax():
            handle = self.post(request, *args, **kwargs)
        else:
            handle = self.http_method_not_allowed(request, *args, **kwargs)
        return handle

    def post(self, request, *args, **kwargs):
        username = request.POST.get('username', '')
        unseed = self.model.objects.get_unseen_notifications(username)
        data = {
            'has_notifications': unseed.count() > 0,
        }
        return JsonResponse(data)
