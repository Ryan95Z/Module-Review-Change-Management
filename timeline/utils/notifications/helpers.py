from timeline.utils.notifications.factory import NotificationFactory


def push_notification(name, **kwargs):
    name = name.lower()
    if len(name) < 1:
        raise ValueError("Name of notification must not be null")

    accepted_names = NotificationFactory.assigned_instances()
    if name not in accepted_names:
        raise ValueError("{} is not a valid notification type".format(name))

    NotificationFactory.makeNotification(name, **kwargs)
