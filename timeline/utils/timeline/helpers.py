from timeline.utils.timeline.factory import EntryFactory


def publish_changes(model, changes_by, entry_name=None, tl_type='Generic'):
    """
    Helper function that will create a confirmed entry of changes
    to the timeline.

    Arguments:
        model           Model to display changes
        changes_by      User that requested the changes
        entry_name      Optional string of the object name in the factory

    Return:
        TimelineEntry object of changes requested
    """
    if entry_name is None:
        entry_name = "Init" if model.is_new else 'Update'
    entry = EntryFactory.makeEntry(entry_name, model)
    return entry.create_entry(status='Confirmed', requested_by=changes_by, entry_type=tl_type)
