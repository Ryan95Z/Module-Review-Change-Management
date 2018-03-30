from core.models import User, Module
from timeline.models import Watcher
from timeline.utils.notifications.factory import NotificationFactory


def push_notification(name, **kwargs):
    """
    Helper function that will automatically route kwargs
    to the notification that is requested.

    Arguments:
        name        Alis name that is associated with the notification
        kwargs      keyword args. Can be anything as long as it is supported
                    by the notification object that is being requested.

    Return:
        True if the notification was successfully created.
    """
    name = name.lower()
    if len(name) < 1:
        raise ValueError("Name of notification must not be null")

    # check the alis name is already in the factory
    accepted_names = NotificationFactory.assigned_instances()
    if name not in accepted_names:
        raise ValueError("{} is not a valid notification type".format(name))

    # make the notification
    NotificationFactory.makeNotification(name, **kwargs)
    return True


class WatcherWrapper(object):
    """
    Wrapper class for the Watcher model. Makes it easier to add
    and remove modules for a particular user.
    """
    model = Watcher

    def __init__(self, user):
        """
        Constructor for WatcherWrapper

        Arguments:
            user        Core User object whose modules are going
                        to be managed.
        """

        # check that it the User object
        if not isinstance(user, User):
            raise ValueError("user needs to be of type core:User")

        # public instance variable
        self.user = user

        # private instance variable
        self.__watcher = self.__get_watcher()

    def __str__(self):
        return "Managing {}".format(self.user.username)

    def add_module(self, module):
        """
        Method to add a single module to watch list for user.

        Arguments:
            module         Either a string of the module code or
                           a Module object

        Return:
            True if was added successfully. False implies module code
            provided does not exist.
        """
        if not isinstance(module, str) and not isinstance(module, Module):
            raise ValueError(
                "module can either be a core:Module object or a module code")

        # if module param is a string, then get the Module object.
        if isinstance(module, str):
            try:
                module = Module.objects.get(module_code=module)
            except Module.DoesNotExist:
                # if the module does not exist, then stop and return false
                return False

        # add the module object to watch list
        self.__watcher.watching.add(module)
        self.__watcher.save()
        return True

    def remove_module(self, module):
        """
        Method to remove a single module from the watch list of a user.

        Arguments:
            module         Either a string of the module code or
                           a Module object

        Return:
            True if was removed successfully. False implies module code
            provided does not exist.
        """
        if not isinstance(module, str) and not isinstance(module, Module):
            raise ValueError(
                "module can either be a core:Module object or a module code")

        # if module param is a string, then get the Module object.
        if isinstance(module, str):
            try:
                module = Module.objects.get(module_code=module)
            except Module.DoesNotExist:
                # if the module does not exist, then stop and return false
                return False

        # remove the module
        self.__watcher.watching.remove(module)
        self.__watcher.save()
        return True

    def bulk_module_add(self, *modules):
        """
        Method that adds a list of modules in one go

        Arguments:
            *modules    any number of module object parameters

        Returns:
            True if successful
        """
        self.__watcher.watching.add(*modules)
        self.__watcher.save()
        return True

    def bulk_module_remove(self, *modules):
        """
        Method that removes a list of modules in one go

        Arguments:
            *modules    any number of module object parameters

        Returns:
            True if successful
        """
        self.__watcher.watching.remove(*modules)
        self.__watcher.save()
        return True

    def modules(self):
        """
        Method that gets all of the modules that are associated
        with this user.

        Arguments:
            void

        Returns:
            Queryset object of Module objects
        """
        return self.__watcher.watching.all()

    # Private methods
    def __get_watcher(self):
        """
        Private method that will get the watcher model object.
        If the user does not have a watcher model associated with
        it, then one is created.

        Arguments:
            void

        Returns:
            Watcher model object
        """
        try:
            return self.model.objects.get(user=self.user)
        except self.model.DoesNotExist:
            return self.model.objects.create(user=self.user)
        except:
            return None
