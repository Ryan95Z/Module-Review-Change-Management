from timeline.utils.timeline.entries import InitEntry, UpdateEntry


class EntryFactory(object):
    """
    Static factory is create different entries to the database
    """
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

    def get(alias):
        """
        Static method to get object from factory.
        """
        if alias is None:
            raise ValueError("alias cannot be None")

        if len(alias) < 1:
            raise ValueError("alias cannot be an empty string")

        try:
            return EntryFactory.factories[alias]
        except KeyError:
            return None

    def makeEntry(alias, model):
        """
        Static method to make a entry object
        """
        if alias is None:
            raise ValueError("alias cannot be None")

        if len(alias) < 1:
            raise ValueError("alias cannot be an empty string")

        if model is None:
            raise ValueError("model cannot be None")
        return EntryFactory.factories[alias](model)
