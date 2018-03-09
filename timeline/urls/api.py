from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from timeline.views import (ConvertMarkdownView)

urlpatterns = [
    url(r'^markdown/$', login_required(
                ConvertMarkdownView.as_view()), name="test"),
]
