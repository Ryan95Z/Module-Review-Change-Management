from django import forms
from django.forms import TextInput, Textarea, NumberInput, Select, CheckboxInput, HiddenInput
from forms.models import ModuleChangeSummary, ModuleTeaching, ModuleAssessment, ModuleReassessment, ModuleSupport, ModuleSoftware

class ModuleChangeSummaryForm(forms.ModelForm):
    """
    Form which handles a tracking form Summary of Changes
    """
    class Meta:
        model = ModuleChangeSummary
        exclude = ('module', 'archive_flag', 'staging_flag', 'current_flag', 'version_number', 'copy_number')
        widgets = {
            'changes_to_outcomes': CheckboxInput(attrs={'data-toggle':'collapse', 'data-target':'#changes_to_outcomes_collapse'}),
            'changes_to_outcomes_desc': Textarea(attrs={'rows':'2', 'class':'form-control form-control-sm'}),
            'changes_to_teaching': CheckboxInput(attrs={'data-toggle':'collapse', 'data-target':'#changes_to_teaching_collapse'}),
            'changes_to_teaching_desc': Textarea(attrs={'rows':'2', 'class':'form-control form-control-sm'}),
            'changes_to_assessments': CheckboxInput(attrs={'data-toggle':'collapse', 'data-target':'#changes_to_assessments_collapse'}),
            'changes_to_assessments_desc': Textarea(attrs={'rows':'2', 'class':'form-control form-control-sm'}),
            'changes_other': CheckboxInput(attrs={'data-toggle':'collapse', 'data-target':'#changes_other_collapse'}),
            'changes_other_desc': Textarea(attrs={'rows':'2', 'class':'form-control form-control-sm'}),
            'changes_rationale': Textarea(attrs={'rows':'2', 'class':'form-control form-control-sm'})
        }

class ModuleTeachingHoursForm(forms.ModelForm):
    """
    Form which handles teaching hours
    """
    class Meta:
        model = ModuleTeaching
        exclude = ('module', 'archive_flag', 'staging_flag', 'current_flag', 'version_number', 'copy_number')

class ModuleSupportForm(forms.ModelForm):
    """
    Form which handles module teaching support details
    """
    class Meta:
        model = ModuleSupport
        exclude = ('module', 'archive_flag', 'staging_flag', 'current_flag', 'version_number', 'copy_number')
        widgets = {
            'lab_support_required': CheckboxInput(attrs={'data-toggle':'collapse', 'data-target':'#lab_support_collapse'}),
            'lab_support_skills': TextInput(attrs={'class':'form-control form-control-sm'}),
            'lab_support_notes': Textarea(attrs={'rows':'3', 'class':'form-control form-control-sm'}),
            'tutorial_support_required': CheckboxInput(attrs={'data-toggle':'collapse', 'data-target':'#tutorial_support_collapse'}),
            'tutorial_support_skills': TextInput(attrs={'class':'form-control form-control-sm'}),
            'tutorial_support_notes': Textarea(attrs={'rows':'3', 'class':'form-control form-control-sm'}),
        }

    def clean(self):
        data = super().clean()
        if data.get('lab_support_required') == True:
            if data.get('lab_support_skills') == '':
                self.add_error('lab_support_skills', 'Must be filled if support is required')

        if data.get('tutorial_support_required') == True:
            if data.get('tutorial_support_skills') == '':
                self.add_error('tutorial_support_skills', 'Must be filled if support is required')
                
        return data
        
class ModuleAssessmentsForm(forms.ModelForm):
    """
    Form which handles module assessment details
    """
    class Meta:
        model = ModuleAssessment
        exclude = ('module', 'archive_flag', 'staging_flag', 'current_flag', 'version_number', 'copy_number')
        widgets = {
            'assessment_id': HiddenInput(),
            'assessment_title': TextInput(attrs={'class':'form-control form-control-sm'}),
            'assessment_type': TextInput(attrs={'class':'form-control form-control-sm'}),
            'assessment_weight': NumberInput(attrs={'class':'form-control form-control-sm'}),
            'assessment_duration': NumberInput(attrs={'class':'form-control form-control-sm'}),
            'assessment_hand_out': Select(attrs={'class':'form-control form-control-sm'}),
            'assessment_hand_in': Select(attrs={'class':'form-control form-control-sm'}),
            'assessment_semester': Select(attrs={'class':'form-control form-control-sm'}),
            'learning_outcomes_covered': Textarea(attrs={'rows': '2', 'class':'form-control form-control-sm'}),
        }

class ModuleReassessmentForm(forms.ModelForm):
    """
    Form which handles module reassessment details
    """
    class Meta:
        model = ModuleReassessment
        exclude = ('module', 'archive_flag', 'staging_flag', 'current_flag', 'version_number', 'copy_number')
        widgets = {
            'reassessment_requested': CheckboxInput(attrs={'data-toggle':'collapse', 'data-target':'#reassessment_collapse'}),
            'reassessment_new_method': TextInput(attrs={'class':'form-control form-control-sm'}),
            'reassessment_rationale': Textarea(attrs={'rows':'2', 'class':'form-control form-control-sm'}),
        }

class ModuleSoftwareForm(forms.ModelForm):
    """
    Form which handles module software requirements
    """
    class Meta:
        model = ModuleSoftware
        exclude = ('module', 'archive_flag', 'staging_flag', 'current_flag', 'version_number', 'copy_number')
        widgets = {
            'software_id': HiddenInput(),
            'software_name': TextInput(attrs={'class':'form-control form-control-sm'}),
            'software_version': TextInput(attrs={'class':'form-control form-control-sm'}),
            'software_packages': TextInput(attrs={'class':'form-control form-control-sm'}),
            'software_additional_comment': TextInput(attrs={'class':'form-control form-control-sm'}),
        }