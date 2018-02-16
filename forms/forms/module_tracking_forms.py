from django import forms
from forms.models import ModuleTeaching, ModuleAssessment, ModuleExam, ModuleSupport, ModuleSoftware

class ModuleTeachingHoursForm(forms.ModelForm):
    """
    Form which handles teaching hours
    """
    class Meta:
        model = ModuleTeaching
        exclude = ('module_code',)

class ModuleSupportForm(forms.ModelForm):
    """
    Form which handles module teaching support details
    """
    class Meta:
        model = ModuleSupport
        exclude = ('module_code',)

class ModuleAssessmentsForm(forms.ModelForm):
    """
    Form which handles module assessment details
    """
    class Meta:
        model = ModuleAssessment
        exclude = ('module_code',)

class ModuleSoftwareForm(forms.ModelForm):
    """
    Form which handles module software requirements
    """
    class Meta:
        model = ModuleSoftware
        exclude = ('module_code',)