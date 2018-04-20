from django.views import View
from django.views.generic.detail import DetailView
from core.views.mixins import LoggedInTestMixin
from django.shortcuts import render, redirect
from django.core.exceptions import ObjectDoesNotExist
from django.forms import formset_factory, modelformset_factory

from core.models import Module
from forms.models.tracking_form import ModuleChangeSummary, ModuleTeaching, ModuleSupport, ModuleAssessment, ModuleReassessment, ModuleSoftware
from forms.forms import ModuleChangeSummaryForm, ModuleTeachingHoursForm, ModuleSupportForm, ModuleAssessmentsForm, ModuleReassessmentForm, ModuleSoftwareForm
from forms.utils.tracking_form import *

from timeline.utils.timeline.tracking_form import tracking_to_timeline, get_form_version_number

from recommenderSystem.forms import ModuleSoftwareSearchForm

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

        softwareSearch_form = ModuleSoftwareSearchForm(instance=ModuleSoftware.objects.filter(module=module, current_flag=True).first())

        # Get a list of all the unbound forms
        unbound_forms = get_unbound_forms(
            change_summary = change_summary_form,
            teaching_hours = teaching_hours_form,
            support = support_form,
            assessment = assessment_forms,
            reassessment = reassessment_form,
            software = software_forms,
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
            'software_forms': software_forms,
            'softwareSearch_form': softwareSearch_form
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
            software_forms.is_valid(),
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
            change_summary_object.current_flag = False
            change_summary_object.staging_flag = True
            if not change_summary_object.is_new:
                change_summary_object.copy_number += 1
            change_summary_form.save()

            teaching_hours_object.module = module
            teaching_hours_object.current_flag = False
            teaching_hours_object.staging_flag = True
            if not teaching_hours_object.is_new:
                teaching_hours_object.copy_number += 1
            teaching_hours_object.save()

            support_object.module = module
            support_object.current_flag = False
            support_object.staging_flag = True
            if not support_object.is_new:
                support_object.copy_number += 1
            support_object.save()

            reassessment_object.module = module
            reassessment_object.current_flag = False
            reassessment_object.staging_flag = True
            if not reassessment_object.is_new:
                reassessment_object.copy_number += 1
            reassessment_object.save()

            for assessment in assessment_objects:
                assessment.module = module
                assessment.current_flag = False
                assessment.staging_flag = True
                if not assessment.is_new:
                    assessment.copy_number += 1
                assessment.save()
            # For Timeline to work, the assessment objects list needs to include all objects, not just edited/new ones.
            # So I work out which weren't edited and add them to the list of objects at the end
            for cleaned_data in assessment_forms.cleaned_data:
                obj = cleaned_data.get("assessment_id", None)
                if not obj in assessment_objects and not obj == None:
                    obj.current_flag=False
                    obj.staging_flag=True
                    obj.save()
                    assessment_objects.append(obj)
            current_assessments = ModuleAssessment.objects.filter(module=module, current_flag=True)
            for assessment in current_assessments:
                if not assessment in assessment_objects:
                    assessment.delete()

            for software in software_objects:
                software.module = module
                software.current_flag = False
                software.staging_flag = True
                if not software.is_new:
                    software.copy_number += 1
                software.save()
            # For Timeline to work, the software objects list needs to include all objects, not just edited/new ones.
            # So I work out which weren't edited and add them to the list of objects at the end
            for cleaned_data in software_forms.cleaned_data:
                obj = cleaned_data.get("software_id", None)
                if not obj in software_objects and not obj == None:
                    obj.current_flag=False
                    obj.staging_flag=True
                    obj.save()
                    software_objects.append(obj)
            current_software = ModuleSoftware.objects.filter(module=module, current_flag=True)
            for software in current_software:
                if not software in software_objects:
                    software.delete()

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
                'software_forms': software_forms,
                'softwareSearch_form': softwareSearch_form
            }
            return render(request, 'module_tracking_form.html', context=error_context)

class LeaderModuleTrackingFormArchive(View):
    def __init__(self):
        super(LeaderModuleTrackingFormArchive, self).__init__()
        self.assessment_formset = modelformset_factory(ModuleAssessment, form=ModuleAssessmentsForm, extra=0)
        self.software_formset = modelformset_factory(ModuleSoftware, form=ModuleSoftwareForm, extra=0)

    def get(self, request, **kwargs):
        """
        GET method which retireves an old tracking form version and displays it in a disabled form
        """
        # Getting varibales from the url
        module_pk = kwargs.get('pk')
        version = kwargs.get('id')
        module = Module.objects.get(pk=module_pk)

        # Setting flags
        form_exists = True
        edit_form = False

        # Gathering existing data and creating the forms. If no value is found for the model filter, None is returned to the instance
        change_summary_form = ModuleChangeSummaryForm(instance=ModuleChangeSummary.objects.filter(module=module, copy_number=version).first())
        teaching_hours_form = ModuleTeachingHoursForm(instance=ModuleTeaching.objects.filter(module=module, copy_number=version).first())
        support_form = ModuleSupportForm(instance=ModuleSupport.objects.filter(module=module, copy_number=version).first())
        reassessment_form = ModuleReassessmentForm(instance=ModuleReassessment.objects.filter(module=module, copy_number=version).first())
        assessment_forms = self.assessment_formset(prefix='assessment_form', queryset=ModuleAssessment.objects.filter(module=module, copy_number=version))
        software_forms = self.software_formset(prefix='software_form', queryset=ModuleSoftware.objects.filter(module=module, copy_number=version))
        softwareSearch_form = ModuleSoftwareSearchForm(instance=ModuleSoftware.objects.filter(module=module, copy_number=version).first())

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
            'software_forms': software_forms,
            'softwareSearch_form': softwareSearch_form
        }
        return render(request, 'module_tracking_form.html', context)
