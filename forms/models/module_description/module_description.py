from django.db import models
from django.utils import timezone

from core.models import Module
from forms.models.module_description import ModuleDescriptionFormVersion
from timeline.models.integrate.entry import TLEntry

class ModuleDescriptionManager(models.Manager):
    """
    Manager for the module description object
    """
    def create_new(self, module, form_version):
        """
        Create a new ModuleDescription and assign it to a given
        module and form version
        """
        return ModuleDescription.objects.create(
            module_id=module.pk,
            form_version=form_version,
        )

    def get_most_recent(self, module):
        """
        Return the most recent ModuleDescription for a given module
        """
        return ModuleDescription.objects.filter(module_id=module).latest('creation_date')

class ModuleDescription(TLEntry):
    """
    Represents an instance of a module description 
    """
    form_version = models.ForeignKey(ModuleDescriptionFormVersion, on_delete=models.PROTECT)

    objects = ModuleDescriptionManager()

    def __str__(self):
        description_phase = "?"
        if(self.archive_flag): description_phase = "Archived"
        if(self.current_flag): description_phase = "Current"
        if(self.staging_flag): description_phase = "Staged"
        return "{} Module Description master for {}".format(description_phase, self.module_id)

    def title(self):
        return "Module Description"