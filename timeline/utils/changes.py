from django.apps import apps
from timeline.models import TableChange
from django.db.models import ForeignKey

# this is temporary for the time
# until I make the timeline dynamic
MODEL_LOCATION = 'core'


def have_changes(model_pk):
    changes = TableChange.objects.filter(model_id=model_pk)
    return len(changes)


def process_changes(entry_pk):
    changes = TableChange.objects.filter(related_entry=entry_pk)
    for change in changes:
        model = apps.get_model(
            app_label=MODEL_LOCATION,
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
