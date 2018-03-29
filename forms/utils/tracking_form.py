from forms.models import ModuleTeaching, ModuleSupport, ModuleAssessment, ModuleSoftware
from forms.forms import ModuleTeachingHoursForm, ModuleSupportForm, ModuleAssessmentsForm, ModuleSoftwareForm
from django.shortcuts import get_object_or_404

def populate_tracking_forms(module_pk):
    teaching_hours = ModuleTeaching.objects.get(module=module_pk)
    support = ModuleSupport.objects.get(module=module_pk)

    teaching_hours_form = ModuleTeachingHoursForm(instance=teaching_hours)
    support_form = ModuleSupportForm(instance=support)

    return teaching_hours_form, support_form