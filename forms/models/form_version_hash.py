from django.db import models

class FormVersionHash(models.Model):
    """
    Represents the hash of a number of form field entities
    """
    hash_string = models.CharField(primary_key=True)
    hash_creation_date = models.DateField()