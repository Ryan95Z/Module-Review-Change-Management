from django.views import View
from django.http import HttpResponse
from django.shortcuts import render, redirect

from core.models import Module
from forms.models.tracking_form import ModuleChangeSummary, ModuleTeaching, ModuleSupport, ModuleAssessment, ModuleReassessment, ModuleSoftware
from forms.forms import ModuleChangeSummaryForm, ModuleTeachingHoursForm, ModuleSupportForm, ModuleAssessmentsForm, ModuleReassessmentForm, ModuleSoftwareForm
from recommenderSystem.forms import ModuleSoftwareSearchForm
from forms.utils.tracking_form import *

# software search form view
class searchBar(View):
    def get(self, request, *args, **kwargs):
        # Get the search term
        search_term = request.GET.get('search_term')
        #  __contains gets translated by Django into a SQL LIKE statement
        items = ModuleSoftware.objects.filter(software_name__icontains=search_term)
        # use json module to return a JSON object to the frontend of each row matching the search term
        return HttpResponse(json.dumps({ # return any module_software where the software name containes the search term
        # create an object that we can send to the frontend
            'results': [
            # dictionary with the data we need (wrap it in a python dictionary and put them into results)
            {
                'software': x.software_name,
                'module': x.module.module_name,
                'module_id': x.module_id,
                'package': x.software_packages,
                'version': x.software_version
            } for x in items] # each x is one item
            }
        ))
