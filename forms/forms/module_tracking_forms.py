from django import forms
from django.forms import TextInput, Textarea, NumberInput, Select, CheckboxInput
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
        widgets = {
            'lab_support_required': CheckboxInput(attrs={'data-toggle':'collapse', 'data-target':'#lab_support_collapse'}),
            'lab_support_skills': TextInput(attrs={'class':'form-control form-control-sm'}),
            'lab_support_notes': Textarea(attrs={'rows':'3', 'class':'form-control form-control-sm'}),
            'tutorial_support_required': CheckboxInput(attrs={'data-toggle':'collapse', 'data-target':'#tutorial_support_collapse'}),
            'tutorial_support_skills': TextInput(attrs={'class':'form-control form-control-sm'}),
            'tutorial_support_notes': Textarea(attrs={'rows':'3', 'class':'form-control form-control-sm'}),
        }
        
class ModuleAssessmentsForm(forms.ModelForm):
    """
    Form which handles module assessment details
    """
    class Meta:
        model = ModuleAssessment
        exclude = ('module_code',)
        widgets = {
            'assessment_title': TextInput(attrs={'class':'form-control form-control-sm'}),
            'assessment_type': TextInput(attrs={'class':'form-control form-control-sm'}),
            'assessment_weight': NumberInput(attrs={'class':'form-control form-control-sm'}),
            'assessment_duration': NumberInput(attrs={'class':'form-control form-control-sm'}),
            'assessment_hand_out': Select(attrs={'class':'form-control form-control-sm'}),
            'assessment_hand_in': Select(attrs={'class':'form-control form-control-sm'}),
            'assessment_semester': Select(attrs={'class':'form-control form-control-sm'}),
            'learning_outcomes_covered': Textarea(attrs={'rows': '2', 'class':'form-control form-control-sm'}),
        }

class ModuleSoftwareForm(forms.ModelForm):
    """
    Form which handles module software requirements
    """
    class Meta:
        model = ModuleSoftware
        exclude = ('module_code',)