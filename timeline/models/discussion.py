from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
from timeline.models import TimelineEntry
from core.models import User


class Discussion(MPTTModel):
    created = models.DateTimeField(auto_now_add=True)
    comment = models.TextField()
    entry = models.ForeignKey(TimelineEntry, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    # mptt field
    parent = TreeForeignKey(
        'self',
        null=True,
        blank=True,
        related_name='replies',
        db_index=True
    )

    class MPTTMeta:
        order_insertion_by = ['created']

    def __str__(self):
        return "{} - {}".format(self.created, self.author)

    def author_username(self):
        return self.author.username

    def author_name(self):
        return self.author.get_full_name()
