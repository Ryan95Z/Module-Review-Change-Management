from django.db import models
from django.db import IntegrityError
from .user import User, UserManager
from .module import Module

class ReviewerManager(object):
    """
    Manager to assist in the creation of Reviewer models
    """
    def __init__(self):
        self.user_manager = UserManager()
        self.user_manager.model = User

    def create_new_reviewer(self, module, username, first_name, last_name,
                         email, password=None):

        # create the basic user
        user = self.user_manager.create_user(
            username=username,
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=password
        )

        # create the reviewer model
        model = self.__create_model(module, user)

        # set the permissions
        user.is_module_reviewer = True
        user.save()
        return model

    def create_reviewer(self, module, user=None):
        """
        Method to create a reviewer from an existing user.
        Will configure the user permissions to be a reviewer.
        """
        if user is None:
            raise ValueError("Must select a user")

        # create the reviewer
        model = self.__create_model(module, user)
        if model is None:
            return None

        # update user permissions now the model has been created.
        user.is_module_reviewer = True
        user.save()
        return model

    def __create_model(self, module, user):
        # Currently the module code is associated with the user via foreign key, which isn't one to one
        # Need to discuss reviewer access
        """
        Private method to actually create the model.
        Could raise the Django IntegrityError if one
        to one relationship is violated.
        """
        if module is None:
            raise ValueError("A module must be included")
        try:
            reviewer = self.model.objects.create(
                module=module,
                reviewer_user=user
            )
            return reviewer
        except IntegrityError:
            return None


class Reviewer(models.Model):
    """
    Model to represent reviewers
    """

    module = models.ForeignKey(Module, on_delete=None)
    reviewer_user = models.OneToOneField(User)

    objects = ReviewerManager()

    def __str__(self):
        return "{} {}".format(self.get_reviewer_name(), self.module)

    def get_reviewer_name(self):
        """
        Method to get the reviewers full name
        """
        return self.reviewer_user.get_full_name()

    def get_reviewer_username(self):
        """
        Method to get the username of the reviewer
        """
        return self.reviewer_user.username

    def get_reviewer_id(self):
        """
        Method to return the id of the user assigned
        to module.
        """
        return self.reviewer_user.id

    class Meta:
        ordering = ['module']