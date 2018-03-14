from timeline.models import Notification
from django.views.generic import View
from django.http import JsonResponse


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
