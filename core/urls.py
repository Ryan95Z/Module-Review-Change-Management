from django.conf.urls import url
from core.views import *

urlpatterns = [
    url(r'^login/', LoginView.as_view(), name='login'),
    url(r'^logout/', LogoutView.as_view(), name='logout'),
    url(r'^all/$', UserListView.as_view(), name='all_users'),
    url(r'^all/edit/(?P<pk>[0-9]+)/$',
        AdminUpdateUserPermissions.as_view(), name='edit_user'),
    url(r'^user/profile/(?P<slug>[\w.@+-]+)/$', UserProfileView.as_view(), name='user_profile')
]
