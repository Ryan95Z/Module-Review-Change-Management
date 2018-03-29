from timeline.utils.timeline.factory import EntryFactory


def publish_changes(model):
    entry_type = "Init" if model.is_new else 'Update'
    entry = EntryFactory.makeEntry(entry_type, model)
    return entry.create_entry(None, 'Generic')
