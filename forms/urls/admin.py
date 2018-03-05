from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from forms.views import *

"""
forms.urls.admin
==================
Contains all of the urls related to the forms features which are for admins
"""

urlpatterns = [
    # view the structure of the most recent form
    url(r'^forms/module_description/$', login_required(
        AdminModuleDescriptionFormStructure.as_view()), name='module_description_form_structure'),
    # view the structure of an older form version
    url(r'^forms/module_description/(?P<pk>[0-9]+)/$', login_required(
        AdminModuleDescriptionFormStructureOld.as_view()), name='old_module_description_form_structure'),
    # edit the structure of the most recent form
    url(r'^forms/module_description/modify/$', login_required(
        AdminModuleDescriptionFormModify.as_view()), name='change_module_description_structure')
]
