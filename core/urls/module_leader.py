from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from core.views import *

"""
urls.module_leader
==================
Contains all of the urls that are only for module leaders. Includes
* Module Descriptions

"""

urlpatterns = [
    # urls for module description forms
    url(r'^modules/(?P<pk>[A-Za-z0-9]+)/description/$', login_required(
        LeaderModuleDescriptionView.as_view()), name='view_module_description')
]