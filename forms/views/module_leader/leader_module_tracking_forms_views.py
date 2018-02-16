from django.views import View
from django.views.generic.detail import DetailView
from core.views.mixins import LoggedInTestMixin
from django.shortcuts import render, redirect

from core.models import Module
from forms.forms import ModuleTeachingHoursForm, ModuleSupportForm, ModuleAssessmentsForm, ModuleSoftwareForm

class LeaderModuleTrackingFormView(DetailView):
    """
    View a module tracking form
    """
    
    model = Module
    template_name="module_tracking_form_view.html"

class LeaderModuleTrackingFormCreate(View):
    """
    Allows module leaders to create new module tracking forms
    """
    def __init__(self):
        super(LeaderModuleTrackingFormCreate, self).__init__()
        self.teaching_hours_form = ModuleTeachingHoursForm
        self.support_form = ModuleSupportForm
        self.assessment_form = ModuleAssessmentsForm
        self.software_form = ModuleSoftwareForm

    def get(self, request, **kwargs):
        """
        GET method which provides the tracking form
        """
        module = Module.objects.get(pk=self.kwargs.get('pk'))
        context = {
            'pk': module.module_code,
            'module': module, 
            'teaching_hours_form': self.teaching_hours_form,
            'support_form': self.support_form,
            'assessment_form': self.assessment_form,
            'software_form': self.software_form
        }
        return render(request, 'module_tracking_form_new.html', context)

    def post(self, request, *args, **kwargs):
        """
        POST method which submits the new tracking form
        """
        module_code = kwargs.get('pk')

        teaching_hours_form = self.teaching_hours_form(request.POST)
        support_form = self.support_form(request.POST)
        assessments_form = self.assessment_form(request.POST)
        software_form = self.software_form(request.POST)
        
        teaching_hours_valid = teaching_hours_form.is_valid()
        support_valid = support_form.is_valid()
        assessments_valid = assessments_form.is_valid()
        software_valid = software_form.is_valid()

        if teaching_hours_valid and support_valid and assessments_valid and software_valid:
            module = Module.objects.get(pk=module_code)

            new_teaching_hours_object = teaching_hours_form.save(commit=False)
            new_support_object = support_form.save(commit=False)
            new_assessment_object = assessments_form.save(commit=False)
            new_software_object = software_form.save(commit=False)

            new_teaching_hours_object.module_code = module
            new_support_object.module_code = module
            new_assessment_object.module_code = module
            new_software_object.module_code = module
            
            new_teaching_hours_object.save()
            new_support_object.save()
            new_assessment_object.save()
            new_software_object.save()

            return redirect('view_module_tracking_form', pk=module_code)
        else:
            print("not valid")
            error_context = {
                'pk': module_code,
                'module': Module.objects.get(pk=module_code), 
                'teaching_hours_form': teaching_hours_form,
                'support_form': support_form,
                'assessment_form': assessment_form,
                'software_form': software_form
            }
            return render(request, 'module_tracking_form_new', context=error_context)