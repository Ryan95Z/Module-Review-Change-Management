from django.views import View
from django.views.generic.detail import DetailView
from core.views.mixins import LoggedInTestMixin
from django.shortcuts import render, redirect
from django.core.exceptions import ObjectDoesNotExist
from django.forms import formset_factory

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
        self.teaching_hours_form = ModuleTeachingHoursForm
        self.support_form = ModuleSupportForm
        self.software_form = ModuleSoftwareForm
        self.assessment_formset = formset_factory(ModuleAssessmentsForm, extra=1, max_num=1)
        self.software_formset = formset_factory(ModuleSoftwareForm, extra=1, max_num=1)

    def get(self, request, **kwargs):
        """
        GET method which provides the tracking form
        """
        module_pk = kwargs.get('pk')
        form_type = kwargs.get('form_type', 'view')
        form_exists = True
        edit_form = True if form_type == 'new' else False

        try:
            self.teaching_hours_form, self.support_form = populate_tracking_forms(module_pk)
        except ObjectDoesNotExist:
            form_exists = False

        try:
            assessments = ModuleAssessment.objects.filter(module_code=module_pk).values()
            assessment_forms = self.assessment_formset(initial=assessments, prefix='assessment_form')
        except ObjectDoesNotExist:
            assessment_forms = self.assessment_formset(None)

        try:
            software = ModuleSoftware.objects.filter(module_code=module_pk).values()
            software_forms = self.software_formset(initial=software, prefix='software_form')
        except ObjectDoesNotExist:
            software_forms = self.software_formset(None)
        

        module = Module.objects.get(pk=self.kwargs.get('pk'))
        context = {
            'edit_form': edit_form,
            'form_exists': form_exists,
            'pk': module.module_code,
            'module': module, 
            'teaching_hours_form': self.teaching_hours_form,
            'support_form': self.support_form,
            'assessment_forms': assessment_forms,
            'software_forms': software_forms
        }
        return render(request, 'module_tracking_form.html', context)

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

            teaching_hours_object = teaching_hours_form.save(commit=False)
            support_object = support_form.save(commit=False)
            assessment_object = assessments_form.save(commit=False)
            software_object = software_form.save(commit=False)

            # teaching_hours_object.module_code = module
            # support_object.module_code = module
            # assessment_object.module_code = module
            # software_object.module_code = module
            
            teaching_hours_object.save()
            support_object.save()
            assessment_object.save()
            software_object.save()

            return redirect('view_module_tracking_form', pk=module_code)
        else:
            error_context = {
                'edit_form': True,
                'form_exists': True,
                'pk': module_code,
                'module': Module.objects.get(pk=module_code), 
                'teaching_hours_form': teaching_hours_form,
                'support_form': support_form,
                'assessment_form': assessments_form,
                'software_form': software_form
            }
            return render(request, 'module_tracking_form.html', context=error_context)