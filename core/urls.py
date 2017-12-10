from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from core.views import *

urlpatterns = [
    url(r'^login/', LoginView.as_view(), name='login'),
    url(r'^logout/', LogoutView.as_view(), name='logout'),
    url(r'^all/$', login_required(UserListView.as_view()), name='all_users'),
    url(r'^all/edit/(?P<pk>[0-9]+)/$', login_required(
        AdminUpdateUserPermissions.as_view()), name='edit_user'),

    url(r'^profile/(?P<slug>[\w.@+-]+)/$',
        login_required(UserSettingsView.as_view()), name='user_settings'),

    url(r'^profile/(?P<slug>[\w.@+-]+)/details/$',
        login_required(UserUpdateDetailsView.as_view()), name='user_details')
]
