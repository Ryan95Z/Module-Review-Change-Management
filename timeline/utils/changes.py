from django.apps import apps
from django.db.models import ForeignKey
from timeline.models import TableChange
from timeline.utils.notifications.helpers import WatcherWrapper


def have_changes(model_pk, instance):
    """
    Function to return any changes that have not been
    commited for a model instance
    """
    if instance is None or model_pk is None:
        raise ValueError("A valid model pk and instance is required")

    model_str = instance.__class__.__name__
    changes = TableChange.objects.filter(
        model_id=model_pk,
        changes_for_model=model_str
    )
    return [c.changes_field for c in changes]


def process_changes(entry_pk):
    """
    Processes the changes for an entry on the timeline.
    """
    if entry_pk is None:
        raise ValueError("entry_pk cannot be None")

    if int(entry_pk) < 1:
        raise ValueError("entry pk needs to be greater than zero.")

    changes = TableChange.objects.filter(related_entry=entry_pk)
    for change in changes:
        model = apps.get_model(
            app_label=change.model_app_label,
            model_name=change.changes_for_model
        )

        item = model.objects.get(pk=change.model_id)

        # field name
        field = change.changes_field

        # get the field type that we need to process
        field_type = model._meta.get_field(field)

        if isinstance(field_type, ForeignKey):
            # if it is a ForeignKey, then we extract the type it wants
            key_object = field_type.rel.to

            # get the object we need to add to update the foreign key
            obj = key_object.objects.get(pk=change.new_value)

            # make the change
            setattr(item, field, obj)

            model = change.changes_for_model
            # Since we are dependent on the module object
            # we can manage the watching of notifications at this level.
            # we look that the field and model is for the module leader
            # then we make the changes
            if field == 'module_leader' and model == 'Module':
                # remove the old module leader from watching module
                old_user = key_object.objects.get(pk=change.current_value)
                old_user_watcher = WatcherWrapper(old_user)
                old_user_watcher.remove_module(change.related_module_code())

                # add the new module leader as a watcher
                new_user_watcher = WatcherWrapper(obj)
                new_user_watcher.add_module(change.related_module_code())
        else:
            # make change to model attribute
            setattr(item, field, change.new_value)

        # override_update prevents an update entry being
        # added when saving the changes
        item.save(override_update=True)

        # remove the change entry
        change.delete()
    return True


def revert_changes(entry_pk):
    """
    Function to remove changes for a entry in the timeline
    """
    if entry_pk is None:
        raise ValueError("entry pk cannot be None")

    if int(entry_pk) < 1:
        raise ValueError("entry pk needs to be greater than zero")

    changes = TableChange.objects.filter(related_entry=entry_pk)

    # check for changes. If there are, the delete each one.
    if changes.count() > 0:
        for change in changes:
            change.delete()
        return True
    return False
