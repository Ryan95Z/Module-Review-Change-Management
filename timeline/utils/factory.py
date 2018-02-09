from timeline.utils.entries import InitEntry, UpdateEntry


class EntryFactory(object):

    def makeEntry(entry_type, module):
        entry_type = entry_type.lower()
        e = None
        if entry_type == 'init':
            e = InitEntry(module)
        elif entry_type == 'update':
            e = UpdateEntry(module)
        return e.create()
