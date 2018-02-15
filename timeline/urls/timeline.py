from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from timeline.views import *

urlpatterns = [
    # view timeline for a particular module
    url(r'^(?P<module_pk>[A-Za-z0-9]+)/$', login_required(
        TimelineListView.as_view()), name="module_timeline"),

    # view to manually change the timeline changes
    url(r'(?P<module_pk>[A-Za-z0-9]+)/update/(?P<pk>[0-9]+)/$',
        login_required(TimelineUpdateView.as_view()), name="entry_edit"),

    url(r'(?P<module_pk>[A-Za-z0-9]+)/approve/(?P<pk>[0-9]+)/$',
        login_required(TimelineUpdateStatus.as_view()), name="approve_entry"),
]
