from django.views import View
from django.views.generic.detail import DetailView
from core.views.mixins import LoggedInTestMixin
from django.shortcuts import render, redirect
from django.core.exceptions import ObjectDoesNotExist
from django.forms import formset_factory, modelformset_factory

from core.models import Module
from forms.models.tracking_form import ModuleChangeSummary, ModuleTeaching, ModuleSupport, ModuleAssessment, ModuleReassessment, ModuleSoftware
from forms.forms import ModuleChangeSummaryForm, ModuleTeachingHoursForm, ModuleSupportForm, ModuleAssessmentsForm, ModuleReassessmentForm, ModuleSoftwareForm
from forms.utils.tracking_form import get_unbound_forms

from timeline.utils.timeline.tracking_form import tracking_to_timeline

class LeaderModuleTrackingForm(View):
    """
    Allows module leaders to view and create tracking forms
    """
    def __init__(self):
        super(LeaderModuleTrackingForm, self).__init__()
        self.assessment_formset = modelformset_factory(ModuleAssessment, form=ModuleAssessmentsForm, extra=1, min_num=1, max_num=1, validate_min=True)
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
        form_exists = True
        edit_form = True if form_type == 'new' else False

        # Gathering existing data and creating the forms. If no value is found for the model filter, None is returned to the instance
        change_summary_form = ModuleChangeSummaryForm(instance=ModuleChangeSummary.objects.filter(module=module, current_flag=True).first())
        teaching_hours_form = ModuleTeachingHoursForm(instance=ModuleTeaching.objects.filter(module=module, current_flag=True).first())
        support_form = ModuleSupportForm(instance=ModuleSupport.objects.filter(module=module, current_flag=True).first())
        reassessment_form = ModuleReassessmentForm(instance=ModuleReassessment.objects.filter(module=module, current_flag=True).first())
        assessment_forms = self.assessment_formset(prefix='assessment_form', queryset=ModuleAssessment.objects.filter(module=module, current_flag=True))
        software_forms = self.software_formset(prefix='software_form', queryset=ModuleSoftware.objects.filter(module=module, current_flag=True))

        # Get a list of all the unbound forms 
        unbound_forms = get_unbound_forms(
            change_summary = change_summary_form,
            teaching_hours = teaching_hours_form,
            support = support_form,
            assessment = assessment_forms,
            reassessment = reassessment_form,
            software = software_forms
        )

        # If absolutely no forms are abound, we assume that one doesn't exist, and set the form_exists flag to False
        if len(unbound_forms) >= 6:
            form_exists = False

        # Setting the context
        context = {
            'edit_form': edit_form,
            'form_exists': form_exists,
            'pk': module_pk,
            'module': module,
            'unbound_forms': unbound_forms,
            'change_summary_form': change_summary_form,
            'teaching_hours_form': teaching_hours_form,
            'support_form': support_form,
            'assessment_forms': assessment_forms,
            'reassessment_form': reassessment_form,
            'software_forms': software_forms
        }
        return render(request, 'module_tracking_form.html', context)

    def post(self, request, *args, **kwargs):
        """
        POST method which submits the new tracking form
        """
        module_pk = kwargs.get('pk')
        module = Module.objects.get(pk=module_pk)

        # Gathering all of the POST data and putting it into its forms. Supply instance data if it exists
        change_summary_form = ModuleChangeSummaryForm(request.POST, instance=ModuleChangeSummary.objects.filter(module=module, current_flag=True).first())
        teaching_hours_form = ModuleTeachingHoursForm(request.POST, instance=ModuleTeaching.objects.filter(module=module, current_flag=True).first())
        support_form = ModuleSupportForm(request.POST, instance=ModuleSupport.objects.filter(module=module, current_flag=True).first())
        reassessment_form = ModuleReassessmentForm(request.POST, instance=ModuleReassessment.objects.filter(module=module, current_flag=True).first())
        assessment_forms = self.assessment_formset(request.POST, prefix="assessment_form") # Doesn't need instance because there is an id associated with each form
        software_forms = self.software_formset(request.POST, prefix="software_form")

        # Run all of the validation
        valid = [
            change_summary_form.is_valid(),
            teaching_hours_form.is_valid(),
            support_form.is_valid(),
            assessment_forms.is_valid(),
            reassessment_form.is_valid(),
            software_forms.is_valid()
        ]

        # If all forms are valid, save to the database
        if all(valid):

            change_summary_object = change_summary_form.save(commit=False)
            teaching_hours_object = teaching_hours_form.save(commit=False)
            support_object = support_form.save(commit=False)
            assessment_objects = assessment_forms.save(commit=False)
            reassessment_object = reassessment_form.save(commit=False)
            software_objects = software_forms.save(commit=False)

            change_summary_object.module = module
            change_summary_object.current_flag = True
            change_summary_form.save()

            teaching_hours_object.module = module
            teaching_hours_object.current_flag = True
            teaching_hours_object.save()

            support_object.module = module
            support_object.current_flag = True
            support_object.save()

            reassessment_object.module = module
            reassessment_object.current_flag = True
            reassessment_object.save()

            for assessment in assessment_objects:
                assessment.module = module
                assessment.current_flag = True
                assessment.save()

            for software in software_objects:
                software.module = module
                software.current_flag = True
                software.save()

            # this makes the timeline
            tracking_to_timeline(
                module.module_code,
                request.user,
                change_summary_object,
                teaching_hours_object,
                support_object,
                assessment_objects,
                reassessment_object,
                software_objects
            )

            return redirect('view_module_tracking_form', pk=module_pk)
        else:
            error_context = {
                'edit_form': True,
                'form_exists': True,
                'pk': module_pk,
                'module': Module.objects.get(pk=module_pk), 
                'change_summary_form': change_summary_form,
                'teaching_hours_form': teaching_hours_form,
                'support_form': support_form,
                'assessment_forms': assessment_forms,
                'reassessment_form': reassessment_form,
                'software_forms': software_forms
            }
            return render(request, 'module_tracking_form.html', context=error_context)