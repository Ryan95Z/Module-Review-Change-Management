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
    # software recommender urls
    url(r'^software-search/$', login_required(
        software_search_ajax), name='software_search'),
    # urls for module description forms
    url(r'^modules/(?P<pk>[A-Za-z0-9]+)/description/view/$', login_required(
        LeaderModuleDescriptionView.as_view()), name='view_module_description'),
    url(r'^modules/(?P<pk>[A-Za-z0-9]+)/description/update/$', login_required(
        LeaderModuleDescriptionView.as_view()), kwargs={'form_type': 'new'}, name='update_module_description'),

    # urls for module tracking forms
    url(r'^modules/(?P<pk>[A-Za-z0-9]+)/tracking-form/view/$', login_required(
        LeaderModuleTrackingForm.as_view()), kwargs={'form_type': 'view'}, name='view_module_tracking_form'),
    url(r'^modules/(?P<pk>[A-Za-z0-9]+)/tracking-form/new/$', login_required(
        LeaderModuleTrackingForm.as_view()), kwargs={'form_type': 'new'}, name='new_module_tracking_form'),
    url(r'^modules/(?P<pk>[A-Za-z0-9]+)/tracking-form/archive/(?P<id>[0-9]+)$', login_required(
        LeaderModuleTrackingFormArchive.as_view()), name='view_archive_tracking_form')

]
