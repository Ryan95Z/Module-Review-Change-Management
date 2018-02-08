from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from timeline.views import *

urlpatterns = [
    url(r'^(?P<module_pk>[A-Za-z0-9]+)/$', login_required(
        TimelineListView.as_view()), name="module_timeline"),
]
