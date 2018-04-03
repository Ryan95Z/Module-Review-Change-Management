from abc import ABC, abstractmethod
from forms.models.module_description import *

def md_to_form(queryset):
    """
    Accepts a queryset of module description entries
    and converts them into the correct format to be
    displayed in a module description form.

    Only works if the given entries correlate to the
    form which is being rendered.
    """
    form_data = {}
    for entry in queryset:
        field = entry.field_id
        id_for_form = "field_entity_" + str(field.pk)
        field_type = field.entity_type
        form_data[id_for_form] = entry.string_entry
    return form_data

class AbstractModuleDescriptionClass(ABC):
    """
    Abstract Module Description Class
    """
    def __init__(self, module, module_description_master):
        self.module = module 
        self.module_description_master=module_description_master
        self.form = FormFieldEntity.objects.get_form(module_description_master.form_version.pk)
        self.values_queryset = ModuleDescriptionEntry.objects.get_full_description(self.module_description_master)

    def get_data_with_labels(self):
        data = {}
        for field in self.form:
            field_id = field.entity_id
            field_label = field.entity_label
            field_type = field.entity_type
            if field_type in ("text-input", "text-area", "multi-choice", "radio-buttons"):
                field_data = self.values_queryset.get(field_id=field_id).string_entry
            elif field_type in ("check-boxes"):
                field_data = self.values_queryset.get(field_id=field_id).boolean_entry
            data[field_label] = field_data
        return data

class ModuleDescriptionClass(AbstractModuleDescriptionClass):
    """
    The module description with the given id
    """
    def __init__(self, module_description):
        module = module_description.module
        super(ModuleDescriptionClass, self).__init__(module, module_description)

class CurrentModuleDescriptionClass(AbstractModuleDescriptionClass):
    """
    The most recent Module Description for a given module
    """
    def __init__(self, module):
        current_module_description = ModuleDescription.objects.get_most_recent(module)
        super(CurrentModuleDescriptionClass, self).__init__(module, current_module_description)