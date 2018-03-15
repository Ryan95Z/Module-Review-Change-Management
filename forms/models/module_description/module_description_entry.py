from django.db import models

from forms.models.module_description import FormFieldEntity, ModuleDescription

class ModuleDescriptionEntryManager(models.Manager):
    """
    Manager for the MD entry model
    """
    def create_new_entry(self, md_id, field_id, entry):
        if isinstance(entry, str):
            return self.create(
                module_description_id=md_id,
                field_id=field_id,
                string_entry=entry)
        elif isinstance(entry, int):
            return self.create(
                module_description_id=md_id,
                field_id=field_id,
                integer_entry=entry)

class ModuleDescriptionEntry(models.Model):
    """
    Represents the answer to a single field within a module description
    """
    module_description_id = models.ForeignKey(ModuleDescription)
    field_id = models.ForeignKey(FormFieldEntity)
    boolean_entry = models.NullBooleanField(null=True)
    string_entry = models.CharField(null=True, max_length = 2000)
    integer_entry = models.IntegerField(null=True)

    objects = ModuleDescriptionEntryManager()

