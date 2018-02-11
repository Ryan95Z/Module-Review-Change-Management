from django.views import View
from django.views.generic.detail import DetailView
from core.views.mixins import LoggedInTestMixin
from django.shortcuts import render, redirect

from core.models import Module
from forms.forms import ModuleTeachingHoursForm, ModuleAssessmentsForm

class LeaderModuleTrackingFormView(DetailView):
    """
    View a module tracking form
    """
    
    model = Module
    template_name="module_tracking_form_view.html"

class LeaderModuleTrackingFormCreate(LoggedInTestMixin, View):
    """
    Allows module leaders to create new module tracking forms
    """
    def get(self, request):
        """
        GET method which provides the tracking form
        """
        teaching_hours_form = ModuleTeachingHoursForm()
        assessment_form = ModuleAssessmentsForm()
        context = {'pk': request.context.pk, 'teaching_hours_form': teaching_hours_form, 'assessment_form': assessment_form}
        return render(request, 'module_tracking_form_new.html', context)

    def post(self, request, *args, **kwargs):
        """
        POST method which submits the new tracking form
        """
        teaching_hours_form = ModuleTeachingHoursForm(request.POST)
        assessments_form = ModuleAssessmentsForm(request.POST)
        
        teaching_hours_valid = teaching_hours_form.is_valid()
        assessments_valid = assessments_form.is_valid()

        if teaching_hours_valid and assessments_valid:
            teaching_hours_form.module_code = request.context.pk
            assessments_form.module_code = request.context.pk
            
            teaching_hours_form.save()
            assessments_form.save()

            return redirect('view_module_tracking_form', pk=request.context.pk)

