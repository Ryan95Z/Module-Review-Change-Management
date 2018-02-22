from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from core.models import User, Module

ENTRY_STATUS = (
    ('Draft', 'Draft'),
    ('Staged', 'Staged'),
    ('Confirmed', 'Confirmed')
)

ENTRY_TYPE = (
    ('Generic', 'Generic'),
    ('Init', 'Init'),
    ('Update', 'Update')
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

    module_code = models.CharField(max_length=10)

    status = models.CharField(
        max_length=9,
        choices=ENTRY_STATUS,
        default='Draft'
    )

    entry_type = models.CharField(
        max_length=6,
        choices=ENTRY_TYPE,
        default="Generic"
    )

    # attributes for generic relation
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.CharField(max_length=10)
    content_object = GenericForeignKey('content_type', 'object_id')

    approved_by = models.ForeignKey(User, blank=True, null=True)

    def __str__(self):
        return "{}@{}".format(self.title, self.created)

    def approver_username(self):
        """
        Method to get the approver's username.
        """
        if self.approved_by is None:
            return None
        return self.approved_by.username

    def approver_name(self):
        """
        Method to get the approver's fullname.
        """
        if self.approved_by is None:
            return None
        return self.approved_by.get_full_name()

    class Meta:
        ordering = ['-created']
