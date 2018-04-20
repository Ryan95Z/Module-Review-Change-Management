from django import forms
from django.forms import TextInput, Textarea, NumberInput, Select, CheckboxInput, HiddenInput
from forms.models import ModuleChangeSummary, ModuleTeaching, ModuleAssessment, ModuleReassessment, ModuleSupport, ModuleSoftware

# add the search form for software recommendations - waad part
class ModuleSoftwareSearchForm(forms.ModelForm):
    """
    Form which suggest/recommend module software requirements
    """

    # hotfix to stop software name from being required. This shouldn't really be a model form, but oh well.
    def __init__(self, *args, **kwargs):
        super(ModuleSoftwareSearchForm, self).__init__(*args, **kwargs)
        self.fields['software_name'].required = False

    class Meta:
        model = ModuleSoftware
        exclude = ('module', 'archive_flag', 'staging_flag', 'current_flag', 'version_number', 'copy_number', 'software_version', 'software_packages', 'software_additional_comment', 'software_tags')
        widgets = {
            'software_id': HiddenInput(),
            'software_name': TextInput(attrs={'class':'form-control form-control-sm'}),
        }
