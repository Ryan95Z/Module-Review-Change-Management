from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from core.views import *


urlpatterns = [
    url(r'^$', login_required(
        ModuleLeaderModuleList.as_view()), name='module_leader_modules'),
]
