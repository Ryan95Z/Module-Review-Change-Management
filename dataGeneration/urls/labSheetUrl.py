from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from core.views import *
from django.views.generic import TemplateView
from dataGeneration.views import *
# from forms.models import ModuleAssessment,ModuleSoftware,ModuleExam,ModuleSupport, ModuleTeaching,ModuleDescription
# from core.models import Module

urlpatterns = [
    url(r'^labSheetPage/$', login_required(labSheetView.as_view()), name='labSheetView'),
    url(r'^labSheetDownload/$', login_required(labSheetDownload.as_view()), name='labSheetDownload'),
]
