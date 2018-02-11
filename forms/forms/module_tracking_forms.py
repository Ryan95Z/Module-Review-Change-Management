from django import forms
from forms.models import ModuleTeaching, ModuleAssessment

class ModuleTeachingHoursForm(forms.ModelForm):
    """
    Form which handles teaching hours
    """
    class Meta:
        model = ModuleTeaching
        exclude = ('module_code',)

class ModuleAssessmentsForm(forms.ModelForm):
    """
    Form which handles module assessment details
    """
    class Meta:
        model = ModuleAssessment
        exclude = ('module_code',)