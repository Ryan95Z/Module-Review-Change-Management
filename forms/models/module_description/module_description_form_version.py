from datetime import datetime
from django.utils import timezone
from django.db import models

class ModuleDescriptionFormVersionManager(models.Manager):
    """
    Manager for the form version model
    """
    def create_new_version(self):
        version = self.create(creation_date=timezone.now())
        return version

    def get_most_recent(self):
        return ModuleDescriptionFormVersion.objects.latest('creation_date')

    def get_version_list(self):
        return ModuleDescriptionFormVersion.objects.all().order_by('-creation_date')

class ModuleDescriptionFormVersion(models.Model):
    """
    Represents the hash of a number of form field entities
    """
    module_description_version = models.AutoField(primary_key=True)
    creation_date = models.DateTimeField()
    
    objects = ModuleDescriptionFormVersionManager()

    def __str__(self):
        return "Module Description Form created on: {}".format(self.creation_date)
