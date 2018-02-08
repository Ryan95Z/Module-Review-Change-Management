from django.db import models
from core.models import User, Module


class TimelineEntry(models.Model):
    title = models.CharField(max_length=30)
    changes = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    module = models.ForeignKey(Module, on_delete=models.CASCADE)

    def __str__(self):
        return "{}@{}".format(self.title, self.created)

    def module_code(self):
        return self.module.module_code

    def module_name(self):
        return self.module.module_name

    class Meta:
        ordering = ['-created']
