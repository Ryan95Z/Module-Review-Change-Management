from django.views import View
from django.views.generic.detail import DetailView
from core.views.mixins import LoggedInTestMixin
from django.shortcuts import render, redirect
from django.core.exceptions import ObjectDoesNotExist
from django.forms import formset_factory, modelformset_factory

from core.models import Module
from forms.models.tracking_form import ModuleTeaching, ModuleSupport, ModuleAssessment, ModuleSoftware
from forms.forms import ModuleTeachingHoursForm, ModuleSupportForm, ModuleAssessmentsForm, ModuleSoftwareForm
from forms.utils.tracking_form import populate_tracking_forms

class LeaderModuleTrackingForm(View):
    """
    Allows module leaders to view and create tracking forms
    """
    def __init__(self):
        super(LeaderModuleTrackingForm, self).__init__()
        self.assessment_formset = modelformset_factory(ModuleAssessment, form=ModuleAssessmentsForm, extra=1, max_num=1)
        self.software_formset = modelformset_factory(ModuleSoftware, form=ModuleSoftwareForm, extra=1, max_num=1)

    def get(self, request, **kwargs):
        """
        GET method which provides the tracking form
        """
        # Getting varibales from the url
        module_pk = kwargs.get('pk')
        module = Module.objects.get(pk=module_pk)
        form_type = kwargs.get('form_type', 'view')

        # Setting flags
        form_errors = []
        form_exists = True
        edit_form = True if form_type == 'new' else False

        # Gathering existing data. If nothing is found, create empty forms
        try:
            teaching_hours = ModuleTeaching.objects.get(module=module, current_flag=True)
            teaching_hours_form = ModuleTeachingHoursForm(instance=teaching_hours)
        except ObjectDoesNotExist:
            teaching_hours_form = ModuleTeachingHoursForm()
            form_errors.append("Teaching Hours")
  
        try:
            support = ModuleSupport.objects.get(module=module, current_flag=True)
            support_form = ModuleSupportForm(instance=support)
        except ObjectDoesNotExist:
            support_form = ModuleSupportForm()
            form_errors.append("Teaching Support")

        try:
            assessments = ModuleAssessment.objects.get_current_assessments(module)
            assessment_forms = self.assessment_formset(queryset=assessments, prefix='assessment_form')
        except ObjectDoesNotExist:
            assessment_forms = self.assessment_formset()
            form_errors.append("Assessments")

        try:
            software = ModuleSoftware.objects.get_current_software(module)
            software_forms = self.software_formset(queryset=software, prefix='software_form')
        except ObjectDoesNotExist:
            software_forms = self.software_formset(None)
            form_errors.append("Software Requirements")

        # If absolutely no data is found, we set the form_exists flag to false
        if len(form_errors) > 3:
            form_exists = False

        # Setting the context
        context = {
            'edit_form': edit_form,
            'form_errors': form_errors,
            'form_exists': form_exists,
            'pk': module_pk,
            'module': module, 
            'teaching_hours_form': teaching_hours_form,
            'support_form': support_form,
            'assessment_forms': assessment_forms,
            'software_forms': software_forms
        }
        return render(request, 'module_tracking_form.html', context)

    def post(self, request, *args, **kwargs):
        """
        POST method which submits the new tracking form
        """
        module_pk = kwargs.get('pk')

        teaching_hours_form = self.teaching_hours_form(request.POST)
        support_form = self.support_form(request.POST)
        assessments_form = self.assessment_form(request.POST)
        software_form = self.software_form(request.POST)
        
        teaching_hours_valid = teaching_hours_form.is_valid()
        support_valid = support_form.is_valid()
        assessments_valid = assessments_form.is_valid()
        software_valid = software_form.is_valid()

        if teaching_hours_valid and support_valid and assessments_valid and software_valid:
            module = Module.objects.get(pk=module_pk)

            teaching_hours_object = teaching_hours_form.save(commit=False)
            support_object = support_form.save(commit=False)
            assessment_object = assessments_form.save(commit=False)
            software_object = software_form.save(commit=False)

            # teaching_hours_object.module_pk = module
            # support_object.module_pk = module
            # assessment_object.module_pk = module
            # software_object.module_pk = module
            
            teaching_hours_object.save()
            support_object.save()
            assessment_object.save()
            software_object.save()

            return redirect('view_module_tracking_form', pk=module_pk)
        else:
            error_context = {
                'edit_form': True,
                'form_exists': True,
                'pk': module_pk,
                'module': Module.objects.get(pk=module_pk), 
                'teaching_hours_form': teaching_hours_form,
                'support_form': support_form,
                'assessment_form': assessments_form,
                'software_form': software_form
            }
            return render(request, 'module_tracking_form.html', context=error_context)