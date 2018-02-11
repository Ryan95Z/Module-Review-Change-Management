from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from forms.views import *

"""
urls.module_leader
==================
Contains all of the urls that are only for module leaders. Includes
* Module Descriptions

"""

urlpatterns = [
    # urls for module description forms
    url(r'^modules/(?P<pk>[A-Za-z0-9]+)/description/view/$', login_required(
        LeaderModuleDescriptionView.as_view()), name='view_module_description'),
    # url(r'^modules/(?P<pk>[A-Za-z0-9]+)/new/$', login_required(
    #     LeaderModuleDescriptionCreateView.as_view()), name='new_module_description')

    # urls for module tracking forms
    url(r'^modules/(?P<pk>[A-Za-z0-9]+)/tracking-form/view/$', login_required(
        LeaderModuleTrackingFormView.as_view()), name='view_module_tracking_form')
]