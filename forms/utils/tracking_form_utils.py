from forms.models import ModuleTeaching, ModuleSupport, ModuleAssessment, ModuleSoftware
from forms.forms import ModuleTeachingHoursForm, ModuleSupportForm, ModuleAssessmentsForm, ModuleSoftwareForm
from django.shortcuts import get_object_or_404

def populate_tracking_forms(module_pk):
    teaching_hours = get_object_or_404(ModuleTeaching, module_code=module_pk)
    support = get_object_or_404(ModuleSupport, module_code=module_pk)
    assessment = get_object_or_404(ModuleAssessment, module_code=module_pk)
    software = get_object_or_404(ModuleSoftware, module_code=module_pk)

    teaching_hours_form = ModuleTeachingHoursForm(instance=teaching_hours)
    support_form = ModuleSupportForm(instance=support)
    assessment_form = ModuleAssessmentsForm(instance=assessment)
    software_form = ModuleSoftwareForm(instance=software)

    return teaching_hours_form, support_form, assessment_form, software_form