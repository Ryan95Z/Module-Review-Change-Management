from django import forms
from django.forms import ModelForm
from core.models import Module

class ModuleDetailForm(ModelForm):
    class Meta:
        model = Module
        exclude = ['module_code']
        labels = {
            'module_name': 'Title',
            'module_credits': 'Credits',
            'module_level': 'Level',
        }
    
    def __init__(self, *args, **kwargs):
        super(ModuleDetailForm, self).__init__(*args, **kwargs)
        self.fields['module_code_dummy'].initial=self.instance.module_code

    module_code_dummy = forms.CharField(
        widget=forms.TextInput(attrs={'disabled':True}),
        required=False
    )
