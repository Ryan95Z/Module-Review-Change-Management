from abc import ABC, abstractmethod
from core.models import Module, User
from timeline.models import TimelineEntry, TableChange
from timeline.utils.factory import EntryFactory


class BaseEntry(ABC):
    """
    Base class for entry types
    """
    def __init__(self, model):
        # public variables
        self.model = model
        self.title = None
        self.type = "Generic"

        # protected variable
        self._tl_entry = TimelineEntry

    @abstractmethod
    def create(self, instance):
        """
        Abstract method to create an entry on the timeline.
        Requires an instance as a parameter.
        """
        pass

    @abstractmethod
    def factory(self):
        """
        Abstract method that is used to
        create new objects when passed to the factory.
        """
        pass

    def _extract_fields(self):
        """
        Protected method to extract all
        of the field names from the model assigned
        to the class.
        """
        fields = [field.name for field in self.model._meta.get_fields()]
        return fields

    def _process_changes(self, changes, entry, instance):
        cls_name = instance.__class__.__name__
        for field, values in changes.items():
            current = values[0]
            change = values[1]

            TableChange.objects.create(
                changes_for_model=cls_name,
                model_id=instance.pk,
                changes_field=field,
                current_value=current,
                new_value=change,
                related_entry=entry,
            )


class InitEntry(BaseEntry):

    def __init__(self, model):
        super(InitEntry, self).__init__(model)
        self.title = "{} created"
        self.type = "Init"

    def create(self, instance):
        fields = self._extract_fields()
        title = self.title.format(instance.module_code)
        md = ""
        for field in fields:
            try:
                value = getattr(instance, field)
                field_string = field.replace("_", " ")
                md += "* {}: {}\n".format(field_string, value)
            except AttributeError:
                pass
        entry = self._tl_entry.objects.create(
            title=title,
            changes=md,
            status="Confirmed",
            module=instance,
            entry_type=self.type
        )
        return entry

    def factory(self):
        """
        Factory implementation to create object
        """
        return self.__class__(self.model)


class UpdatedEntry(BaseEntry):

    def __init__(self, model):
        super(UpdatedEntry, self).__init__(model)
        self.title = "Changes to {}:\n\n"
        self.type = "Update"

    def create(self, instance):
        fields = self._extract_fields()
        diff = instance.differences()
        title = self.title.format(instance.module_code)

        entry = None
        md = ""
        if bool(diff):

            # loop through changes and process into markdown
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

            entry = self._tl_entry.objects.create(
                title=title,
                changes=md,
                module=instance,
                entry_type=self.type
            )

            self._process_changes(diff, entry, instance)
            return entry
        return entry

    def factory(self):
        """
        Factory implementation to create object
        """
        return self.__class__(self.model)


# register the classes to the factory
EntryFactory.register(InitEntry, "init", Module)
EntryFactory.register(UpdatedEntry, "update", Module)
