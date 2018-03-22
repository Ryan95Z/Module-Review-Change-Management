from django.db import models
from core.models import Module
from timeline.models.integrate import BaseTimelineNode


class TLEntry(BaseTimelineNode):
    module = models.ForeignKey(Module, on_delete=models.CASCADE)

    class Meta:
        abstract = True

    def module_code(self):
        return self.module.module_code
