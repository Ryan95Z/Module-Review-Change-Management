from datetime import datetime
from django.utils import timezone
from django.db import models

class ModuleDescriptionFormVersionManager(models.Manager):
    """
    Manager for ModuleDescriptionFormVersion
    """
    def create_new_version(self):
        """
        Returns a new instance of a form structure and sets the creation date to now
        """
        version = self.create(creation_date=timezone.now())
        return version

    def get_most_recent(self):
        """
        Returns the most recent module description form version
        """
        return ModuleDescriptionFormVersion.objects.latest('creation_date')

    def get_version_list(self):
        """
        Returns a list of all form versions, ordered by creation date, new to old
        """
        return ModuleDescriptionFormVersion.objects.all().order_by('-creation_date')

class ModuleDescriptionFormVersion(models.Model):
    """
    Represents an instance of a the ModuleDescription form structure
    """
    module_description_version = models.AutoField(primary_key=True)
    creation_date = models.DateTimeField()
    
    objects = ModuleDescriptionFormVersionManager()

    def __str__(self):
        return "Module Description Form created on: {}".format(self.creation_date)
