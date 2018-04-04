from abc import ABC, abstractmethod
from django.core.exceptions import ObjectDoesNotExist

from forms.models.module_description import *
from forms.forms import ModuleDescriptionForm

class AbstractModuleDescriptionWrapper(ABC):
    """
    Abstract Module Description Class
    """
    def __init__(self, module, module_description_master):
        self.module = module 
        self.module_description_master=module_description_master
        self.form_master = module_description_master.form_version
        self.form = FormFieldEntity.objects.get_form(self.form_master.pk)
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
    
    def get_form(self, post_data=False):
        form_data = {}
        for entry in self.values_queryset:
            field = entry.field_id
            id_for_form = "field_entity_" + str(field.pk)
            field_type = field.entity_type
            form_data[id_for_form] = entry.string_entry
        if post_data:
            return ModuleDescriptionForm(post_data, md_version=self.form_master.pk, initial=form_data)
        else:
            return ModuleDescriptionForm(md_version=self.form_master.pk, initial=form_data)

class ModuleDescriptionWrapper(AbstractModuleDescriptionWrapper):
    """
    The module description with the given id
    """
    def __init__(self, module_description):
        module = module_description.module
        super(ModuleDescriptionWrapper, self).__init__(module, module_description)

class CurrentModuleDescriptionWrapper(AbstractModuleDescriptionWrapper):
    """
    The most recent Module Description for a given module
    """
    def __init__(self, module):
        current_module_description = ModuleDescription.objects.get_most_recent(module)
        super(CurrentModuleDescriptionWrapper, self).__init__(module, current_module_description)