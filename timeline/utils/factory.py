from timeline.utils.entries import InitEntry


class EntryFactory(object):
    def makeEntry(entry_type, module):
        entry_type = entry_type.lower()
        e = None
        if entry_type == 'init':
            e = InitEntry(module)
        e.create()
