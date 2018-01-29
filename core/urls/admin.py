from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from core.views import *

"""
urls.admin
==================
Contains all of the urls that are only for the admins. Includes
* Users
* Year Tutors
* Modules

"""

urlpatterns = [
    # urls for accessing admin parts
    url(r'^all/$', login_required(UserListView.as_view()), name='all_users'),
    url(r'^all/edit/(?P<pk>[0-9]+)/$', login_required(
        AdminUpdateUserPermissions.as_view()), name='edit_user'),
    url(r'^all/new/', login_required(
        AdminNewUserView.as_view()), name='new_user'),

    # year tutor urls
    url(r'^tutors/$', login_required(
        AdminYearTutorListView.as_view()), name='all_tutors'),
    url(r'^tutors/new/', login_required(
        AdminYearTutorCreateView.as_view()), name='new_tutor'),
    url(r'^tutors/(?P<pk>[0-9]+)/$', login_required(
            AdminYearTutorUpdateView.as_view()), name="update_tutor"),

    # module urls
    url(r'^modules/$', login_required(
        AdminModuleListView.as_view()), name='all_modules'),
    url(r'^modules/new/$', login_required(
        AdminModuleCreateView.as_view()), name='new_module'),
    url(r'^modules/(?P<pk>[A-Za-z0-9]+)/$', login_required(
        AdminModuleUpdateView.as_view()), name='update_module'),
]
