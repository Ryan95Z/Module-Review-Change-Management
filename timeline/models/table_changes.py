from django.db import models
from timeline.models import TimelineEntry
from core.models import Module


class TableChange(models.Model):
    changes_for_model = models.CharField(max_length=30)
    model_id = models.CharField(max_length=30)
    changes_field = models.CharField(max_length=30)
    current_value = models.CharField(max_length=50)
    new_value = models.CharField(max_length=50)

    related_entry = models.ForeignKey(
        TimelineEntry,
        on_delete=models.CASCADE,
    )

    def related_module_code(self):
        return self.entry.module_code
