from timeline.models import TimelineEntry
from timeline.utils.timeline.factory import EntryFactory
from timeline.utils.timeline.entries import UPDATE


def tracking_to_timeline(module_code, changes_by, *args):
    """
    Helper function that contains the process to create timeline
    entries for the tracking form.
    """
    processer = ProcessTrackingForm(*args)
    return processer.create_entries(module_code, changes_by)


def get_form_version_number(parent_id):
    entry = TimelineEntry.objects.filter(parent_entry_id=parent_id).first()
    revert = entry.revert_object_id
    model = entry.content_object.__class__
    try:
        return model.objects.get(pk=revert).version_number
    except model.DoesNotExist:
        return 1


class ProcessTrackingForm(object):
    """
    Class that will process the models and generate
    a parent and set of child entries.
    """

    def __init__(self, *args):
        self.models = []

        # flattern the args list to be a list of django models.
        for model in args:
            if isinstance(model, list):
                self.models += model
            else:
                self.models.append(model)

    def _object_type(self, model):
        """
        Method to filter which entry should be used.
        """
        if model.is_new:
            return "Init"
        return "Update"

    def prepare(self):
        """
        Method to get the relevant entry objects
        """
        entries = []
        for m in self.models:
            entry = self._object_type(m)

            # get the entry from the factory
            entries.append(EntryFactory.makeEntry(entry, m))
        return entries

    def create_entries(self, module_code, changes_by):
        """
        Creates the parent and child entries for the tracking form.
        """
        entries = self.prepare()
        parent = ParentEntry(module_code, changes_by, *entries)
        parent.create_parent_entry()


class ParentEntry(object):
    """
    Bespoke class that is just used to handle the generation
    of a parent and child entries for the tracking form.
    """
    def __init__(self, module_code, changes_by, *args):
        self.args = args
        self.module_code = module_code
        self.changes_by = changes_by

    def create_parent_entry(self):
        """
        Method that creates the parent entry with
        a number of children entries.
        """
        title = "Changes to tracking form"
        content = "Changes to tracking form:\n\n"
        module_code = self.module_code
        object_id = 0
        content_object = None

        # changes flag, used to determine if the parent
        # should be created.
        changes = 0

        # loop through each model and get the summary
        for model in self.args:
            if model.have_changes():
                content += "* {}\n".format(model.sum_changes())
                changes += 1

        # if there are no changes
        if changes < 1:
            return None

        # make the parent entry
        parent = TimelineEntry.objects.create(
            title=title,
            changes=content,
            module_code=module_code,
            object_id=object_id,
            content_object=content_object,
            changes_by=self.changes_by,
            entry_type='Tracking-Form'
        )

        self.__generate_child_entries(parent)
        return parent

    def __generate_child_entries(self, parent):
        for model in self.args:
            if model.type_of_entry() == UPDATE:
                base = model.get_original_data()
                cls = model.model_class_object()

                del base['module']
                base['current_flag'] = False
                base['archive_flag'] = True
                base['version_number'] = base['copy_number']
                base['module_id'] = model.get_module_code()

                copy = cls.objects.create(**base)
                model.create_entry(
                    parent=parent,
                    entry_type='Tracking-Form',
                    revert=copy.pk
                )
            else:
                model.create_entry(
                    parent=parent,
                    entry_type='Tracking-Form'
                )
