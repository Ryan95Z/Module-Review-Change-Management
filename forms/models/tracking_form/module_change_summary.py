from django.db import models
from timeline.models.integrate.entry import TLEntry

class ModuleChangeSummary(TLEntry):
    """
    Model which represents the "Summary of Changes" section of the tracking form
    """
    changes_to_outcomes = models.BooleanField(
        default=False, 
        verbose_name="Changes to learning outcomes and/or syllabus")
    changes_to_outcomes_desc = models.TextField(
        blank=True,
        max_length=750)
    changes_to_teaching = models.BooleanField(
        default=False, 
        verbose_name="Changes to method of teaching (e.g. number of lectures, labs, tutorials, etc.")
    changes_to_teaching_desc = models.TextField(
        blank=True,
        max_length=750)
    changes_to_assessments = models.BooleanField(
        default=False, 
        verbose_name="Changes to assessments")
    changes_to_assessments_desc = models.TextField(
        blank=True,
        max_length=750)
    changes_other = models.BooleanField(
        default=False, 
        verbose_name="Any other changes")
    changes_other_desc = models.TextField(
        blank=True,
        max_length=750)
    changes_rationale = models.TextField(
        blank=True,
        max_length=1000,
        verbose_name="Rationale for changes - please provide a full explanation of the reason for changes")

    archive_flag = models.BooleanField(default=False)
    staging_flag = models.BooleanField(default=False)
    current_flag = models.BooleanField(default=False)
    version_number = models.IntegerField(default=1)
    copy_number = models.IntegerField(default=1)

    def __str__(self):
        return "Summary of changes for {}".format(self.module)

    def title(self):
        return "Summary of Changes"