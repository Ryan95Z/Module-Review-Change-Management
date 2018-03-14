from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from timeline.views import (ConvertMarkdownView, GetNotifications)

urlpatterns = [
    url(r'^markdown/$', login_required(
                ConvertMarkdownView.as_view()), name="api_markdown"),

    url(r'^notifications/$', login_required(
        GetNotifications.as_view()), name="api_notifications"),
]
