from timeline.utils.timeline.entries import InitEntry, UpdateEntry


class EntryFactory(object):
    factories = {
        'Init': InitEntry,
        'Update': UpdateEntry
    }

    def assigned_instances():
        """
        Static method that returns a list of the objects
        that can be created.
        """
        return list(EntryFactory.factories.keys())

    def get(alis):
        """
        Static method to get object from factory.
        """
        return EntryFactory.factories[alis]

    def makeEntry(alis, model):
        return EntryFactory.factories[alis](model)
