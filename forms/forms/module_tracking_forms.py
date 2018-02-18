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

    lab_support_required = forms.BooleanField(
        widget=forms.CheckboxInput(attrs={'class':'form-check-input'}))
    lab_support_skills = forms.CharField(
        widget=forms.TextInput(attrs={'class':'form-control form-control-sm'}))
    lab_support_notes = forms.CharField(
        widget=forms.Textarea(attrs={'rows':'3', 'class':'form-control form-control-sm'}))
    tutorial_support_required = forms.BooleanField(
        widget=forms.CheckboxInput(attrs={'class':'form-check-input'}))
    tutorial_support_skills = forms.CharField(
        widget=forms.TextInput(attrs={'class':'form-control form-control-sm'}))
    tutorial_support_notes = forms.CharField(
        widget=forms.Textarea(attrs={'rows':'3', 'class':'form-control form-control-sm'}))
        
class ModuleAssessmentsForm(forms.ModelForm):
    """
    Form which handles module assessment details
    """
    class Meta:
        model = ModuleAssessment
        exclude = ('module_code',)

    learning_outcomes_covered = forms.CharField(
        widget=forms.Textarea(attrs={'rows': '3'})
    )

class ModuleSoftwareForm(forms.ModelForm):
    """
    Form which handles module software requirements
    """
    class Meta:
        model = ModuleSoftware
        exclude = ('module_code',)