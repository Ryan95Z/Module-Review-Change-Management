from django.db import models
from django.db import IntegrityError
from .user import User, UserManager
from .module import Module

class ReviewerManager(object):
    """
    Manager to assist in the creation of Reviewer models
    Module(s) must be stored in a list
    """
    def __init__(self):
        self.user_manager = UserManager()
        self.user_manager.model = User

    def create_new_reviewer(self, modules, username, first_name, last_name,
                         email, password=None):

        if not isinstance(modules, (list,)):
            modules = [modules]

        # create the basic user
        user = self.user_manager.create_user(
            username=username,
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=password
        )

        # create the reviewer model
        model = self.__create_model(modules, user)

        # set the permissions
        user.is_module_reviewer = True
        user.save()
        return model

    def create_reviewer(self, modules, user=None):
        """
        Method to create a reviewer from an existing user.
        Will configure the user permissions to be a reviewer.
        Accepts a list of module objects and a user object
        """
        if modules is None:
            raise ValueError("At least one module must be selected")
        if user is None:
            raise ValueError("Must select a user")
        if not isinstance(modules, (list,)):
            modules = [modules]

        # create the reviewer
        model = self.__create_model(modules, user)
        if model is None:
            return None

        # update user permissions now the model has been created.
        user.is_module_reviewer = True
        user.save()
        return model

    def __create_model(self, modules, user):
        try:
            reviewer = self.model.objects.create(user=user)
            reviewer.save()
            for module in modules:
                reviewer.modules.add(module)
            return reviewer
        except IntegrityError:
            return None


class Reviewer(models.Model):
    """
    Model to represent reviewers
    """
    
    user = models.OneToOneField(User)
    modules = models.ManyToManyField(Module)

    objects = ReviewerManager()

    def __str__(self):
        return "{} - {}".format(self.get_reviewer_name(), self.get_reviewer_modules_list())

    def get_reviewer_name(self):
        """
        Method to get the reviewers full name
        """
        return self.user.get_full_name()

    def get_reviewer_username(self):
        """
        Method to get the username of the reviewer
        """
        return self.user.username

    def get_reviewer_id(self):
        """
        Method to return the id of the user assigned
        to module.
        """
        return self.user.id

    def get_reviewer_modules_list(self):
        """
        Returns a comma seperated list of the modules which this user
        is the reviewer of
        """

        module_list = []
        for module in self.modules.all():
            module_list.append(module.module_code)

        return ", ".join(module_list)

    class Meta:
        ordering = ['user']