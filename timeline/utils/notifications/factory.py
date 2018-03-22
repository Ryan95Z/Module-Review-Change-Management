class NotificationFactory(object):
    # dictioanry to store registered factories
    factories = {}

    def register(cls, alis):
        # create the object
        instance = cls()

        # add it to the factory
        NotificationFactory.factories[alis] = instance.factory()

    def assigned_instances():
        """
        Static method that returns a list of the objects
        that can be created.
        """
        return list(NotificationFactory.factories.keys())

    def get(alis):
        """
        Static method to get object from factory.
        """
        return NotificationFactory.factories[alis]

    def makeNotification(alis, **kwargs):
        notices = NotificationFactory.get(alis)
        notices.create(**kwargs)
