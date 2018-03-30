from django.db import models
from timeline.models.integrate.entry import TLEntry

class ModuleReassessment(TLEntry):
    """
    Model which tracks the method of reassessment for a module
    """
    reassessment_requested = models.BooleanField(
        default=False, 
        verbose_name="Request change of reassessment method")
    reassessment_new_method = models.CharField(
        blank=True,
        max_length=200, 
        verbose_name="New reassessment method")
    reassessment_rationale = models.TextField(
        blank=True,
        max_length=750)

    archive_flag = models.BooleanField(default=False)
    staging_flag = models.BooleanField(default=False)
    current_flag = models.BooleanField(default=False)
    version_number = models.IntegerField(default=1)

    def __str__(self):
        return "Reassessment details for {}".format(self.module)

    def title(self):
        return "Reassessment Details"