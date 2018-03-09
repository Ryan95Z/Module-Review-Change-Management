from abc import ABC, abstractmethod
from django.db.models import ForeignKey, ManyToManyField
from timeline.models import TimelineEntry, TableChange
from timeline.models.integrate import BaseTimelineNode
from timeline.models.integrate.entry import TLEntry


class BaseEntry(ABC):
    """
    Base class for entry types
    """
    def __init__(self, model):
        if model is None:
            raise ValueError("model cannot be None.")

        # check that model inherits BaseTimelineNode
        if not issubclass(model, BaseTimelineNode):
            raise ValueError("model needs to inherit from BaseTimelineNode")

        # public variables
        self.model = model
        self.model_app_label = self.model._meta.app_label
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

    """
    Protected methods
    """
    def _extract_fields(self):
        """
        Method to extract all
        of the field names from the model assigned
        to the class.
        """
        fields = [field.name for field in self.model._meta.get_fields()]
        # remove created from fields as not needed for timline.
        try:
            fields.remove('created')
            fields.remove('id')
            fields.remove('module')
        except:
            pass
        return fields

    def _get_module_code(self, instance):
        """
        Method to extract module code from the model
        """
        module_code = None
        cls = instance.__class__
        if issubclass(cls, TLEntry):
            module_code = instance.pk
            module_code = instance.module_code()
        else:
            module_code = instance.pk
        return module_code

    def _object_id(self, instance):
        """
        Method to get the primary key from model instance
        """
        return getattr(instance, instance._meta.pk.name)

    def _process_changes(self, changes, entry, instance):
        """
        Method to process the changes for a timeline entry
        """
        if instance is None or not isinstance(instance, self.model):
            raise ValueError("instance must not be None")

        if entry is None or not isinstance(entry, self._tl_entry):
            raise ValueError("entry for timeline must not be None")

        # loop through changes and create table
        # change entries for them.
        cls_name = instance.__class__.__name__
        for field, values in changes.items():
            current = values[0]
            change = values[1]

            TableChange.objects.create(
                changes_for_model=cls_name,
                model_id=instance.pk,
                model_app_label=self.model_app_label,
                changes_field=field,
                current_value=current,
                new_value=change,
                related_entry=entry,
            )


class InitEntry(BaseEntry):
    """
    Timeline entry for when a new model instance is added.
    """
    def __init__(self, model):
        super(InitEntry, self).__init__(model)
        self.title = "{} created"
        self.type = "Init"

    def create(self, instance):
        """
        Method to create an new model instanace entry
        """
        if instance is None or not isinstance(instance, self.model):
            raise ValueError("instance must not be None")

        fields = self._extract_fields()
        title = self.title.format(instance.title())
        md = ""
        for field in fields:

            field_type = self.model._meta.get_field(field)
            if isinstance(field_type, ManyToManyField):
                # Prevents ManyToMany relationships being display in
                # the timeline. This has occured due to the way
                # the save operations are performed by a ManyToManyField.
                # It works by having an internal manager that saves changes
                # within the field object and is not connected to any
                # public methods that can find these changes.
                continue

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
            module_code=self._get_module_code(instance),
            object_id=self._object_id(instance),
            content_object=instance,
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
        self.title = "Changes to {}\n\n"
        self.type = "Update"

    def create(self, instance):
        """
        Method to create an updated entry
        """
        if instance is None or not isinstance(instance, self.model):
            raise ValueError("instance must not be None")

        diff = instance.differences()
        title = self.title.format(instance.title())

        entry = None
        md = ""
        if bool(diff):

            # loop through changes and process into markdown
            for field, values in diff.items():
                field_str = field.replace("_", " ")
                orignal = values[0]
                updated = values[1]

                # check if field is a foreign key. This is done
                # to allow for extraction of data from the object it expects.
                field_type = self.model._meta.get_field(field)
                if isinstance(field_type, ForeignKey):
                    key_object = field_type.rel.to
                    orignal = key_object.objects.get(pk=values[0])
                    updated = key_object.objects.get(pk=values[1])

                # create the markdown for it
                md += "* {}: {} => {}\n".format(field_str, orignal, updated)

            # create the entry
            entry = self._tl_entry.objects.create(
                title=title,
                changes=md,
                module_code=self._get_module_code(instance),
                object_id=self._object_id(instance),
                content_object=instance,
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
