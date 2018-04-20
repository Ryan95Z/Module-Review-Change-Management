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
        new_desc = ModuleDescription(
            module_id=module.pk,
            form_version=form_version,
            creation_date=timezone.now(),
            current_flag=True
        )
        new_desc.save(force_insert=True)
        return new_desc

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
    creation_date = models.DateTimeField()

    archive_flag = models.BooleanField(default=False)
    staging_flag = models.BooleanField(default=False)
    current_flag = models.BooleanField(default=False)

    objects = ModuleDescriptionManager()

    def __str__(self):
        description_phase = "?"
        if(self.archive_flag): description_phase = "Archived"
        if(self.current_flag): description_phase = "Current"
        if(self.staging_flag): description_phase = "Staged"
        return "{} Module Description master for {}".format(description_phase, self.module_id)

    def title(self):
        return "Module Description"