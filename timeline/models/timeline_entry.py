from django.db import models
from core.models import User, Module

ENTRY_STATUS = (
    ('Draft', 'Draft'),
    ('Staged', 'Staged'),
    ('Confirmed', 'Confirmed')
)


class TimelineEntry(models.Model):
    """
    Model to represent a single entry
    for the timeline.
    """
    title = models.CharField(max_length=30)
    changes = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    status = models.CharField(
        max_length=9,
        choices=ENTRY_STATUS,
        default='Draft'
    )

    module = models.ForeignKey(Module, on_delete=models.CASCADE)

    def __str__(self):
        return "{}@{}".format(self.title, self.created)

    def module_code(self):
        """
        Method to get the module code
        associated with entry.
        """
        return self.module.module_code

    def module_name(self):
        """
        Method to get the module name
        associated with the entry.
        """
        return self.module.module_name

    class Meta:
        ordering = ['-created']
