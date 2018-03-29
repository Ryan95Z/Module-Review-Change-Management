from timeline.models import TimelineEntry
from abc import ABC, abstractmethod


def process_changes(module_code, *args):
    entries = []
    for obj in args:
        if not isinstance(obj, list):
            print(obj.is_new)
            if not obj.is_new:
                entries.append(BuildTLEntry(obj))
            else:
                entries.append(InitEntry(obj))
        else:
            for i in obj:
                print(i.is_new)
                if not i.is_new:
                    entries.append(BuildTLEntry(i))
                else:
                    entries.append(InitEntry(i))

    p = ParentEntry(module_code, *entries)
    p.create_master()


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
    def create_entry(self, parent):
        pass

    def module_code(self):
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

    def create_entry(self, parent):
        title = self.model.title()
        changes = self.content()
        module_code = self.module_code()
        object_id = self.model.pk
        content_object = self.model

        return TimelineEntry.objects.create(
            title=title,
            changes=changes,
            module_code=module_code,
            object_id=object_id,
            content_object=content_object,
            parent_entry=parent,
            entry_type='Tracking-Form'
        )


class BuildTLEntry(BaseEntry):
    def __init__(self, model):
        super(BuildTLEntry, self).__init__(model)

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

    def create_entry(self, parent):
        if not self.have_changes():
            return

        title = self.model.title()
        changes = self.content()
        module_code = self.module_code()
        object_id = self.model.pk
        content_object = self.model

        return TimelineEntry.objects.create(
            title=title,
            changes=changes,
            module_code=module_code,
            object_id=object_id,
            content_object=content_object,
            parent_entry=parent,
            entry_type='Tracking-Form'
        )


class ParentEntry(object):
    def __init__(self, module_code, *args):
        self.args = args
        self.module_code = module_code

    def create_master(self):
        title = "Changes to tracking form"
        content = "Changes to tracking form:\n\n"
        module_code = self.module_code
        object_id = 0
        content_object = None

        changes = 0

        for a in self.args:
            if a.have_changes():
                content += "* {}\n".format(a.sum_changes())
                changes += 1

        if changes > 0:
            master = TimelineEntry.objects.create(
                title=title,
                changes=content,
                module_code=module_code,
                object_id=object_id,
                content_object=content_object,
                entry_type='Tracking-Form'
            )

            for a in self.args:
                a.create_entry(master)
