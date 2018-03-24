from core.models import User, Module
from timeline.models import Watcher
from timeline.utils.notifications.factory import NotificationFactory


def push_notification(name, **kwargs):
    name = name.lower()
    if len(name) < 1:
        raise ValueError("Name of notification must not be null")

    accepted_names = NotificationFactory.assigned_instances()
    if name not in accepted_names:
        raise ValueError("{} is not a valid notification type".format(name))

    NotificationFactory.makeNotification(name, **kwargs)


class WatcherWrapper(object):
    model = Watcher

    def __init__(self, user):
        if not isinstance(user, User):
            raise ValueError("user needs to be of type core:User")

        self.user = user
        self.__watcher = self.__get_watcher()

    def __str__(self):
        return "Managing {}".format(self.user.username)

    def add_module(self, module):
        if not isinstance(module, str) and not isinstance(module, Module):
            raise ValueError(
                "module can either be a core:Module object or a module code")

        if isinstance(module, str):
            try:
                module = Module.objects.get(module_code=module)
            except Module.DoesNotExist:
                return False
        self.__watcher.watching.add(module)
        self.__watcher.save()
        return True

    def bulk_module_add(self, *modules):
        self.__watcher.watching.add(*modules)
        self.__watcher.save()

    def bulk_module_remove(self, *modules):
        self.__watcher.watching.remove(*modules)
        self.__watcher.save()

    def remove_module(self, module):
        if not isinstance(module, str) and not isinstance(module, Module):
            raise ValueError(
                "module can either be a core:Module object or a module code")

        if isinstance(module, str):
            try:
                module = Module.objects.get(module_code=module)
            except Module.DoesNotExist:
                return False
        self.__watcher.watching.remove(module)
        self.__watcher.save()
        return True

    def modules(self):
        return self.__watcher.watching.all()

    def __get_watcher(self):
        try:
            return self.model.objects.get(user=self.user)
        except self.model.DoesNotExist:
            return self.model.objects.create(user=self.user)
        except:
            return None
