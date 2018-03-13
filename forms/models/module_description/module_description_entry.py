from django.db import models

from forms.models.module_description import FormFieldEntity, ModuleDescription

class ModuleDescriptionEntry(models.Model):
    """
    Represents the answer to a single field within a module description
    """
    module_description_id = models.ForeignKey(ModuleDescription)
    field_id = models.ForeignKey(FormFieldEntity)
    boolean_entry = models.BooleanField(blank=True)
    string_entry = models.CharField(blank=True, max_length = 2000)
    integer_entry = models.IntegerField(blank=True)

