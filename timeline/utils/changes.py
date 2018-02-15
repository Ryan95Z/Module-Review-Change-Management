from django.apps import apps
from timeline.models import TableChange

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
        setattr(item, change.changes_field, change.new_value)
        item.save(override_update=True)

        change.delete()
