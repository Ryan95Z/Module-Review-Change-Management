from django.db import models
from django.utils import timezone

from core.models import Module
from forms.models.module_description import ModuleDescriptionFormVersion

class ModuleDescriptionManager(models.Manager):
    """
    Manager for the module description object
    """
    def create_new(self, module, form_version):
        """
        Create a new ModuleDescription and assign it to a given
        module and form version
        """
        return self.create(
            module=module, 
            form_version=form_version,
            creation_date=timezone.now())

    def get_most_recent(self, module):
        """
        Return the most recent ModuleDescription for a given module
        """
        return ModuleDescription.objects.filter(module=module).latest('creation_date')

class ModuleDescription(models.Model):
    """
    Represents an instance of a module description 
    """
    module = models.ForeignKey(Module, on_delete=models.CASCADE)
    form_version = models.ForeignKey(ModuleDescriptionFormVersion, on_delete=models.PROTECT)
    creation_date = models.DateTimeField()

    objects = ModuleDescriptionManager()