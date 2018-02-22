
class EntryFactory(object):
    """
    Factory class to create entries for the
    database when requested.
    """

    # dictioanry to store registered factories
    factories = {}

    def register(cls, alis, model):
        """
        Class method to register objects
        to the factory. Provides three parameters

        cls - the class that will be created from factory
        alis - alis string that is used to create objects
        model - the model that needs to be provided with the object
        """

        # create the object
        instance = cls(model)

        # add it to the factory
        EntryFactory.factories[alis] = instance.factory()

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

    def makeEntry(alis, instance):
        """
        Static method to create entries for the timeline.
        """
        e = EntryFactory.get(alis)
        e.create(instance)
