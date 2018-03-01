from django.apps import apps
from timeline.models import TableChange
from django.db.models import ForeignKey


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
    if int(entry_pk) < 1:
        raise ValueError("entry pk needs to be greater than zero")

    changes = TableChange.objects.filter(related_entry=entry_pk)

    # check for changes. If there are, the delete each one.
    if len(changes) > 0:
        for change in changes:
            change.delete()
        return True
    return False
