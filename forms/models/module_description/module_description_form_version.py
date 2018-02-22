from django.db import models

class ModuleDescriptionFormVersion(models.Model):
    """
    Represents the hash of a number of form field entities
    """
    creation_date = models.DateField()