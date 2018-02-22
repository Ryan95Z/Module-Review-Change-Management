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

    # view to cause changes to be made to the model that the
    # timeline is assigned
    url(r'(?P<module_pk>[A-Za-z0-9]+)/approve/(?P<pk>[0-9]+)/$',
        login_required(TimelineUpdateStatus.as_view()), name="approve_entry"),

    # view to remove the changes that are being staged in the timeline
    url(r'(?P<module_pk>[A-Za-z0-9]+)/revert/(?P<pk>[0-9]+)/$',
        login_required(TimelineRevertStage.as_view()), name="revert_entry"),


    # Discussion
    url(r'(?P<module_pk>[A-Za-z0-9]+)/discussion/(?P<pk>[0-9]+)/$',
        login_required(DiscussionView.as_view()), name="discussion"),
]
