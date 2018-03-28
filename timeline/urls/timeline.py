from django.conf.urls import url, include
from django.contrib.auth.decorators import login_required
from timeline.views import (TimelineListView, TimelineUpdateStatus,
                            TimelineRevertStage, DiscussionView,
                            DiscussionUpdateView, DiscussionDeleteView,
                            NotificationHubView, NotificationRedirectView)

urlpatterns = [
    url(r'api/', include('timeline.urls.api')),

    ##############################
    # Notification URLs
    ##############################
    url(r'notifications/$', login_required(
        NotificationHubView.as_view()), name='all_notification'),

    url(r'(?P<pk>[0-9]+)/redirect/$', login_required(
        NotificationRedirectView.as_view()), name='notification_redirect'),


    ##############################
    # Timeline URLs
    ##############################
    # url for viewing the timeline for a particular module
    url(r'^(?P<module_pk>[A-Za-z0-9]+)/$', login_required(
        TimelineListView.as_view()), name="module_timeline"),

    # url for moving a timeline enrty up the workflow process
    url(r'(?P<module_pk>[A-Za-z0-9]+)/approve/(?P<pk>[0-9]+)/$',
        login_required(TimelineUpdateStatus.as_view()), name="approve_entry"),

    # url for moving a timeline entry down the workflow process
    url(r'(?P<module_pk>[A-Za-z0-9]+)/revert/(?P<pk>[0-9]+)/$',
        login_required(TimelineRevertStage.as_view()), name="revert_entry"),

    ##############################
    # Discussion URLs
    ##############################
    # url for viewing a discussion
    url(r'(?P<module_pk>[A-Za-z0-9]+)/discussion/(?P<pk>[0-9]+)/$',
        login_required(DiscussionView.as_view()), name="discussion"),

    # url for editing an individual comment
    url(r'(?P<module_pk>[A-Za-z0-9]+)/discussion/(?P<entry_pk>[0-9]+)'\
        '/edit/(?P<pk>[0-9]+)/$', login_required(
            DiscussionUpdateView.as_view()), name='edit_comment'),

    # url for deleting a individual comment
    url(r'(?P<module_pk>[A-Za-z0-9]+)/discussion/(?P<entry_pk>[0-9]+)'\
        '/delete/(?P<pk>[0-9]+)/$', login_required(
            DiscussionDeleteView.as_view()), name='delete_comment'),
]
