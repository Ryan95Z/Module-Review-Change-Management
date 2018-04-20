from django import forms
from forms.models.module_description import FormFieldEntity

class FieldEntityForm(forms.ModelForm):
    """
    Form used to describe a single entity in the module description form structure
    """
    class Meta:
        model = FormFieldEntity
        exclude = ('entity_id','module_description_version','entity_default')

    def clean(self):
        data = super().clean()
        field_type = data.get('entity_type')
        choices = data.get('entity_choices').strip()

        if field_type in ("multi-choice", "radio-buttons"):
            if choices == '':
                self.add_error('entity_choices', 'Must provide choices seperated by commas')
            elif ',' not in choices:
                self.add_error('entity_choices', 'Must provide at least two options, seperated by commas')
            elif choices.startswith(',') or choices.endswith(','):
                self.add_error('entity_choices', 'Must not start or end with a comma')

        return data