from timeline.models import TimelineEntry
from core.models import Module
from abc import ABC, abstractmethod
import markdown


class BaseEntry(ABC):
    def __init__(self, module):
        self.module = module
        self.model = TimelineEntry
        self.fields = [f.name for f in Module._meta.get_fields()]

    @abstractmethod
    def create(self):
        pass


class InitEntry(BaseEntry):
    def __init__(self, module):
        super(InitEntry, self).__init__(module)
        self.title = "{} created".format(module.module_code)

    def create(self):
        md = "{} contains currently:\n\n".format(self.module.module_name)
        for field in self.fields:
            try:
                v = getattr(self.module, field)
                field_string = field.replace("_", " ")
                md += "* {}: {}\n".format(field_string, v)
            except AttributeError:
                pass
        entry = self.model.objects.create(
            title=self.title,
            changes=md,
            module=self.module
        )
