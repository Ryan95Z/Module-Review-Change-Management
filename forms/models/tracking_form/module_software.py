from django.db import models
from django.core.exceptions import ObjectDoesNotExist

from timeline.register import timeline_register
from timeline.models.integrate.entry import TLEntry
from core.models import Module

class ModuleSoftwareManager(models.Manager):
    """
    Manager for the ModuleSoftware model
    """
    def get_current_software(self, module):
        current_software = self.filter(module=module, current_flag=True)
        if current_software:
            return current_software
        else:
            raise ObjectDoesNotExist('No software with the current_flag exists')

@timeline_register
class ModuleSoftware(TLEntry):
    """
    Model which represents the software requirements for a module
    """
    # Currently all CharField, we need to discuss this model as it has strong ties with
    # the software recommendation stuff
    software_id = models.AutoField(primary_key=True)
    software_name = models.CharField(max_length=50, verbose_name="Software Name")
    software_version = models.CharField(blank=True, max_length=10, verbose_name="Version")
    software_packages = models.CharField(blank=True, max_length=100, verbose_name="Packages")
    software_tags = models.CharField(blank=True, max_length=100)
    software_additional_comment = models.TextField(blank=True, max_length=500, verbose_name="Additional Comments")

    archive_flag = models.BooleanField(default=False)
    staging_flag = models.BooleanField(default=False)
    current_flag = models.BooleanField(default=False)

    objects = ModuleSoftwareManager()

    def __str__(self):
        return "Software requirements for {}".format(self.module)
    
    def title(self):
        return "Software"
