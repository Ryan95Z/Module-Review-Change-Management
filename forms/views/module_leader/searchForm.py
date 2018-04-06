from django.views import View
from django.http import HttpResponse
from django.views.generic.detail import DetailView
from core.views.mixins import LoggedInTestMixin
from django.shortcuts import render, redirect
from django.core.exceptions import ObjectDoesNotExist
from django.forms import formset_factory, modelformset_factory

from core.models import Module
from forms.models.tracking_form import ModuleChangeSummary, ModuleTeaching, ModuleSupport, ModuleAssessment, ModuleReassessment, ModuleSoftware
from forms.forms import ModuleChangeSummaryForm, ModuleTeachingHoursForm, ModuleSupportForm, ModuleAssessmentsForm, ModuleReassessmentForm, ModuleSoftwareForm, ModuleSoftwareSearchForm
from forms.utils.tracking_form import *

from timeline.utils.timeline.tracking_form import tracking_to_timeline, get_form_version_number


# software search form view - waad part
def software_search_ajax(request):
    # Get the search term
    search_term = request.GET.get('search_term')

    items = ModuleSoftware.objects.filter(software_name__icontains=search_term)
    # use json module to return a JSON object to the frontend of each row matching the search term
    return HttpResponse(json.dumps({
        'results': [
        {
            'software': x.software_name,
            'module': x.module.module_name,
            'module_id': x.module_id,

            'package': x.software_packages,
            'version': x.software_version
        } for x in items]
        }
    ))
