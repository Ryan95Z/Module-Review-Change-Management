from django.db import models

from core.models import Module
from forms.models.module_description import ModuleDescriptionFormVersion, ModuleDescriptionEntry

class ModuleDescription(models.Model):
    """
    Represents an instance of a module description 
    """
    module_code = models.ForeignKey(Module, on_delete=models.CASCADE)
    form_version = models.ForeignKey(ModuleDescriptionFormVersion, on_delete=models.PROTECT)
    entries = models.ManyToManyField(ModuleDescriptionEntry)

    class Meta:
        unique_together = (("module_code", "form_version"))

    