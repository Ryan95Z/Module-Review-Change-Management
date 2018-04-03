from timeline.utils.timeline.factory import EntryFactory


def publish_changes(model, changes_by):
    """
    Helper function that will create a confirmed entry of changes
    to the timeline.

    Arguments:
        model           Model to display changes
        changes_by      User that requested the changes

    Return:
        TimelineEntry object of changes requested
    """
    entry_type = "Init" if model.is_new else 'Update'
    entry = EntryFactory.makeEntry(entry_type, model)
    return entry.create_entry(status='Confirmed', requested_by=changes_by)
