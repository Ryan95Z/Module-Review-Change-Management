from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from forms.views import *

"""
forms.urls.admin
==================
Contains all of the urls related to the forms features which are for admins
"""

urlpatterns = [
    # form editing
    url(r'^forms/tracking_form/$', login_required(
        AdminModuleDescriptionFormStructure.as_view()), name='module_description_form_structure'),
    url(r'^forms/module_description/modify/$', login_required(
        AdminModuleDescriptionFormModify.as_view()), name='change_module_description_structure')
]
