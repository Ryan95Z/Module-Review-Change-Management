from timeline.utils.notifications.notices import BaseNotice


class NotificationFactory(object):
    # dictioanry to store registered factories
    factories = {}

    def register(cls, alias):
        if len(alias) < 1:
            raise ValueError("alias provided should not be an empty string")

        if cls is None:
            raise ValueError("Notification class cannot be None")

        if not issubclass(cls, BaseNotice):
            raise ValueError("Notification classes need to inherit BaseNotice")

        # create the object
        instance = cls()

        # add it to the factory
        NotificationFactory.factories[alias] = instance.factory()

    def assigned_instances():
        """
        Static method that returns a list of the objects
        that can be created.
        """
        return list(NotificationFactory.factories.keys())

    def get(alias):
        """
        Static method to get object from factory.
        """
        if len(alias) < 1:
            raise ValueError("alias provided should not be an empty string")
        return NotificationFactory.factories[alias]

    def makeNotification(alias, **kwargs):
        if len(alias) < 1:
            raise ValueError("alias provided should not be an empty string")

        notices = NotificationFactory.get(alias)
        notices.create(**kwargs)
