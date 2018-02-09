import markdown
from timeline.models import TimelineEntry
from core.models import Module, User
from abc import ABC, abstractmethod


class BaseEntry(ABC):
    """
    Abstract base class for various types of entries in the
    module timeline.
    """
    def __init__(self, module):
        if module is None:
            raise ValueError("module must not be none")

        # public instance properties
        self.module = module
        self.model = TimelineEntry

        # extract all possible field names
        self.fields = [field.name for field in Module._meta.get_fields()]

    @abstractmethod
    def create(self):
        """
        Abstract method for creating the entry
        """
        pass


class InitEntry(BaseEntry):
    def __init__(self, module):
        super(InitEntry, self).__init__(module)
        self.title = "{} created".format(module.module_code)
        self.changes = None

    def create(self):
        """
        Method to create an init entry in the timeline for a module.
        Returns the entry that was created.
        """

        md = "{} contains currently:\n\n".format(self.module.module_name)
        for field in self.fields:
            try:
                value = getattr(self.module, field)
                field_string = field.replace("_", " ")
                md += "* {}: {}\n".format(field_string, value)
            except AttributeError:
                pass
        self.changes = md
        entry = self.model.objects.create(
            title=self.title,
            changes=md,
            module=self.module
        )
        return entry


class UpdateEntry(BaseEntry):
    def __init__(self, module):
        super(UpdateEntry, self).__init__(module)
        self.title = "Changes to {}".format(module.module_code)
        self.changes = None

    def create(self):
        """
        Method to create an update entry in the timeline for a module.
        Returns the entry that was created.
        """

        # check for changes in model
        diff = self.module.differences()
        md = "Changes to {}:\n\n".format(self.module.module_code)

        entry = None

        # if there are changes
        if bool(diff):

            # loop through changes and process
            # into markdown
            for field, values in diff.items():
                field_str = field.replace("_", " ")
                orignal = values[0]
                updated = values[1]

                # since module_leader is a foreign key
                # it returns the id when dictionary is provided
                # so we have to explict covert it to be a User.
                if field == 'module_leader':
                    orignal = User.objects.get(id=values[0]).get_full_name()
                    updated = User.objects.get(id=values[1]).get_full_name()

                md += "* {}: {} => {}\n".format(field_str, orignal, updated)

            self.changes = md

            entry = self.model.objects.create(
                title=self.title,
                changes=md,
                module=self.module
            )
            return entry
        return entry
