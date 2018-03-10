from django import forms
from forms.models.module_description import FormFieldEntity

class ModuleDescriptionForm(forms.Form):
    """
    Form which takes a module description version and generates a form based on that specific version
    """
    def __init__(self, *args, **kwargs):
        if 'md_version' in kwargs:
            md_version = kwargs.pop('md_version')
            self.form_entities = FormFieldEntity.objects.get_form(self.md_version)
        else:
            self.form_entities = FormFieldEntity.objects.get_most_recent_form()
        super(ModuleDescriptionForm, self).__init__(*args, **kwargs)

        for entity_number, e in enumerate(self.form_entities):
            entity_type = e.get('entity_type')
            if entity_type == "text-input":
                self.fields['field_%s' % entity_number] = forms.CharField(
                    label=e.get('entity_label'),
                    max_length=e.get('entity_max_length')
                )
            elif entity_type == "text-area":
                self.fields['field_%s' % entity_number] = forms.CharField(
                    widget=forms.Textarea(),
                    label=e.get('entity_label'),
                    max_length=e.get('entity_max_length')
                )
            elif entity_type == "multi-choice":
                self.fields['field_%s' % entity_number] = forms.ChoiceField(
                    choices=[(choice.strip(),choice.strip()) for choice in e.get('entity_choices').split(',')],
                    label=e.get('entity_label'),
                )
            elif entity_type == "check-boxes":
                self.fields['field_%s' % entity_number] = forms.BooleanField(
                    widget=forms.CheckboxInput,
                    label=e.get('entity_label')
                )

            

            


