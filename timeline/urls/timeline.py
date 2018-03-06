from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from timeline.views import (TimelineListView, TimelineUpdateStatus,
                            TimelineRevertStage, DiscussionView,
                            DiscussionUpdateView, DiscussionDeleteView)

urlpatterns = [
    # view timeline for a particular module
    url(r'^(?P<module_pk>[A-Za-z0-9]+)/$', login_required(
        TimelineListView.as_view()), name="module_timeline"),

    # view to cause changes to be made to the model that the
    # timeline is assigned
    url(r'(?P<module_pk>[A-Za-z0-9]+)/approve/(?P<pk>[0-9]+)/$',
        login_required(TimelineUpdateStatus.as_view()), name="approve_entry"),

    # view to remove the changes that are being staged in the timeline
    url(r'(?P<module_pk>[A-Za-z0-9]+)/revert/(?P<pk>[0-9]+)/$',
        login_required(TimelineRevertStage.as_view()), name="revert_entry"),


    # Discussion url
    url(r'(?P<module_pk>[A-Za-z0-9]+)/discussion/(?P<pk>[0-9]+)/$',
        login_required(DiscussionView.as_view()), name="discussion"),

    url(r'(?P<module_pk>[A-Za-z0-9]+)/discussion/(?P<entry_pk>[0-9]+)'\
        '/edit/(?P<pk>[0-9]+)$', login_required(
            DiscussionUpdateView.as_view()), name='edit_comment'),

    url(r'(?P<module_pk>[A-Za-z0-9]+)/discussion/(?P<entry_pk>[0-9]+)'\
        '/delete/(?P<pk>[0-9]+)$', login_required(
            DiscussionDeleteView.as_view()), name='delete_comment')
]
