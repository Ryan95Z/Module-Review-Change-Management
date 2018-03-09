from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from core.views import *

"""
urls.user
==================
Contains URLs that are for all users. Includes
* Login / Logout
* Various profile urls
"""

urlpatterns = [
    url(r'^login/', LoginView.as_view(), name='login'),
    url(r'^logout/', LogoutView.as_view(), name='logout'),

    # generic user profile urls
    url(r'^profile/settings/(?P<slug>[\w.@+-]+)/$',
        login_required(UserSettingsView.as_view()), name='user_settings'),
    url(r'^profile/settings/(?P<slug>[\w.@+-]+)/details/$',
        login_required(UserUpdateDetailsView.as_view()), name='user_details'),

    url(r'^profile/settings/(?P<slug>[\w.@+-]+)/password/$', login_required(
        UserUpdatePasswordView.as_view()), name='user_password'),

    url(r'^profile/(?P<pk>[0-9]+)/$', login_required(
        UserProfileDetailView.as_view()), name='user_profile')
]
