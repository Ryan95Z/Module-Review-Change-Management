from django import forms
from forms.models.module_description import FormFieldEntity, ModuleDescriptionFormVersion

class ModuleDescriptionForm(forms.Form):
    """
    Form which takes a module description version and generates a form based on that specific version
    """
    def __init__(self, *args, **kwargs):
        """
        In order for the form to be dynamic, it must generate all of the fields
        in the initialization of the form.
        """
        # Retrieve the form version from the kwargs, then collect all of the fields
        # we need to create. If there is no version, get the most recent one
        if 'md_version' in kwargs:
            self.md_version = kwargs.pop('md_version')
            self.form_entities = FormFieldEntity.objects.get_form(self.md_version)
        else:
            self.md_version = ModuleDescriptionFormVersion.objects.get_most_recent().module_description_version
            self.form_entities = FormFieldEntity.objects.get_most_recent_form()
        super(ModuleDescriptionForm, self).__init__(*args, **kwargs)

        # Loop through all of the entities and determine what widget to render
        # depending on its type
        for e in self.form_entities:
            entity_type = e.get('entity_type')
            if entity_type == "text-input":
                self.fields['field_entity_%s' % e.get('entity_id')] = forms.CharField(
                    widget=forms.TextInput(attrs={'class':'form-control form-control-sm'}),
                    label=e.get('entity_label'),
                    max_length=e.get('entity_max_length'),
                    required=e.get('entity_required')
                )
            elif entity_type == "text-area":
                self.fields['field_entity_%s' % e.get('entity_id')] = forms.CharField(
                    widget=forms.Textarea(attrs={'rows':'6', 'class':'form-control form-control-sm'}),
                    label=e.get('entity_label'),
                    max_length=e.get('entity_max_length'),
                    required=e.get('entity_required')
                )
            elif entity_type == "multi-choice":
                self.fields['field_entity_%s' % e.get('entity_id')] = forms.ChoiceField(
                    widget=forms.Select(attrs={'class':'form-control form-control-sm'}),
                    choices=[(choice.strip(),choice.strip()) for choice in e.get('entity_choices').split(',')],
                    label=e.get('entity_label'),
                    required=e.get('entity_required')
                )
            elif entity_type == "radio-buttons":
                self.fields['field_entity_%s' % e.get('entity_id')] = forms.ChoiceField(
                    widget=forms.RadioSelect(),
                    choices=[(choice.strip(),choice.strip()) for choice in e.get('entity_choices').split(',')],
                    label=e.get('entity_label'),
                    required=e.get('entity_required')
                )
            elif entity_type == "check-boxes":
                self.fields['field_entity_%s' % e.get('entity_id')] = forms.BooleanField(
                    widget=forms.CheckboxInput,
                    label=e.get('entity_label'),
                    required=e.get('entity_required')
                )

        # Set the form_version. 
        self.fields['form_version'].initial = self.md_version
    
    # Hidden field which can be used to determine which form version this is using
    form_version = forms.IntegerField(
        widget=forms.HiddenInput(),
        required=True)

            

            


