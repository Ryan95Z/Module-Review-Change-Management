from django.db import models
from core.models import User, Module


class TimelineEntry(models.Model):
    title = models.CharField(max_length=30)
    changes = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User)
    module = models.ForeignKey(Module)

    def __str__(self):
        return "{}@{}".format(title, created)

    def created_by_username(self):
        return self.created_by.username

    def created_by_id(self):
        return self.created_by.id

    def module_code(self):
        return self.module.module_code

    def module_name(self):
        return self.module.module_name
