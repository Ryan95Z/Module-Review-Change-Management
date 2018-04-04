from django.db import models

from forms.models.module_description import FormFieldEntity, ModuleDescription

class ModuleDescriptionEntryManager(models.Manager):
    """
    Manager for the ModuleDescriptionEntry model
    """
    def create_new_entry(self, md_id, field_id, entry):
        """
        Creates a new ModuleDescriptionEntry object and links it to
        a ModuleDescription 'parent',and  a FormFieldEntity. 
        """
        # Determines what type the entry is and sets the appropriate field
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

    # Return the values for the most recent module description of a given model
    def get_last_description(self, module):
        last_description = ModuleDescription.objects.get_most_recent(module)
        return ModuleDescriptionEntry.objects.filter(module_description_id=last_description)

    # Returns the values for a module description given it's id
    def get_full_description(self, module_description):
        return self.filter(module_description_id=module_description)
    
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