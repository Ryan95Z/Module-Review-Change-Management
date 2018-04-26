from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from core.views import *
from django.views.generic import TemplateView
from dataGeneration.moduleview import *


urlpatterns = [
    # url(r'^labSheetPage/$', login_required(TemplateView.as_view(template_name='lab_sheet.html')), name='index'),
    url(r'^moduleSheetPage/$', login_required(ModuleSheetView.as_view()), name='ModuleSheetView'),
    url(r'^moduleSheetDownload/$', login_required(ModuleSheetDownload.as_view()), name='ModuleSheetDownload'),
]
