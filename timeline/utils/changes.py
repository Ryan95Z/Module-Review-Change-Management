from django.apps import apps
from timeline.models import TableChange
from django.db.models import ForeignKey

# this is temporary for the time
# until I make the timelien dynamic
MODEL_LOCATION = 'core'


def have_changes(model_pk):
    changes = TableChange.objects.filter(model_id=model_pk)
    return len(changes)


def process_changes(entry_pk):
    changes = TableChange.objects.filter(related_entry=entry_pk)
    for change in changes:
        m = apps.get_model(
            app_label=MODEL_LOCATION,
            model_name=change.changes_for_model
        )

        item = m.objects.get(pk=change.model_id)

        field = change.changes_field

        field_type = m._meta.get_field(field)
        if isinstance(field_type, ForeignKey):
            key_object = field_type.rel.to
            obj = key_object.objects.get(pk=change.new_value)
            setattr(item, field, obj)
        else:
            setattr(item, field, change.new_value)
        
        item.save(override_update=True)
        change.delete()
