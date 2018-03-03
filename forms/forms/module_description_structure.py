from django import forms
from forms.models.module_description import FormFieldEntity

class FieldEntityForm(forms.ModelForm):
    """
    Form used to describe a single entity in the module description form structure
    """
    class Meta:
        model = FormFieldEntity
        exclude = ('entity_id','module_description_version','entity_default')