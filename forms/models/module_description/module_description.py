from django.db import models
from django.utils import timezone

from core.models import Module
from forms.models.module_description import ModuleDescriptionFormVersion

class ModuleDescriptionManager(models.Manager):
    """
    Manager for the module description object
    """

    def create_new(self, module_code, form_verion):
        return self.create(
            module_code=module_code, 
            form_version=form_version,
            creation_date=timezone.now())

class ModuleDescription(models.Model):
    """
    Represents an instance of a module description 
    """
    module_code = models.ForeignKey(Module, on_delete=models.CASCADE)
    form_version = models.ForeignKey(ModuleDescriptionFormVersion, on_delete=models.PROTECT)
    creation_date = models.DateTimeField()

    objects = ModuleDescriptionManager()

    class Meta:
        unique_together = (("module_code", "form_version"))

    