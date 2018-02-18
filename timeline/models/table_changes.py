from django.db import models
from timeline.models import TimelineEntry


class TableChange(models.Model):
    """
    Model to represent changes that are made in the timeline.
    """
    changes_for_model = models.CharField(max_length=30)
    model_id = models.CharField(max_length=30)
    model_app_label = models.CharField(max_length=30)
    changes_field = models.CharField(max_length=30)
    current_value = models.CharField(max_length=50)
    new_value = models.CharField(max_length=50)

    related_entry = models.ForeignKey(
        TimelineEntry,
        on_delete=models.CASCADE,
    )

    def related_module_code(self):
        """
        Method to get the module code for the assigned
        changes.
        """
        return self.related_entry.module_code()
