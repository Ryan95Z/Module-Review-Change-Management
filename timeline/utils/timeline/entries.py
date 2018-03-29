from timeline.models import TimelineEntry
from timeline.models.integrate.entry import TLEntry
from abc import ABC, abstractmethod


class BaseEntry(ABC):
    def __init__(self, model):
        self.model = model
        self.changes = None

    @abstractmethod
    def have_changes(self):
        pass

    @abstractmethod
    def content(self):
        pass

    @abstractmethod
    def create_entry(self, parent, entry_type):
        pass

    def get_module_code(self):
        cls = self.model.__class__
        if not issubclass(cls, TLEntry):
            return self.model.module_code
        return self.model.module_code()

    def title(self):
        return self.model.title()


class InitEntry(BaseEntry):
    def __init__(self, model):
        super(InitEntry, self).__init__(model)

    def have_changes(self):
        return True

    def content(self):
        diff = self.model.differences()

        md = ""
        for field, changes in diff.items():
            field = field.replace("_", " ")
            updated = changes[1]
            md += "* {}: {}\n".format(field, updated)
        return md

    def sum_changes(self):
        return "{} has been created for {}".format(
            self.model.title(),
            self.module_code()
        )

    def create_entry(self, parent, entry_type):
        title = self.model.title()
        changes = self.content()
        module_code = self.get_module_code()
        object_id = self.model.pk
        content_object = self.model

        return TimelineEntry.objects.create(
            title=title,
            changes=changes,
            module_code=module_code,
            object_id=object_id,
            content_object=content_object,
            parent_entry=parent,
            entry_type=entry_type
        )


class UpdateEntry(BaseEntry):
    def __init__(self, model):
        super(UpdateEntry, self).__init__(model)

    def get_differences(self):
        if self.changes is None:
            self.changes = self.model.differences()
        return self.changes

    def have_changes(self):
        return bool(self.get_differences())

    def content(self):
        diff = self.model.differences()
        md = ""
        for field, changes in diff.items():
            field = field.replace("_", " ")
            original = changes[0]
            updated = changes[1]
            md += "* {}: {} -> {}\n".format(field, original, updated)
        return md

    def sum_changes(self):
        n_changes = len(self.get_differences())
        return "There are {} changes to {}".format(
            n_changes, self.model.title()
        )

    def create_entry(self, parent, entry_type):
        if not self.have_changes():
            return

        title = self.model.title()
        changes = self.content()
        module_code = self.get_module_code()
        object_id = self.model.pk
        content_object = self.model

        return TimelineEntry.objects.create(
            title=title,
            changes=changes,
            module_code=module_code,
            object_id=object_id,
            content_object=content_object,
            parent_entry=parent,
            entry_type=entry_type
        )
