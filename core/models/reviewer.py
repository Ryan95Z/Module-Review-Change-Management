from django.db import models
from django.db import IntegrityError
from .user import User, UserManager

# choices for module_code field.
# TEMPORARY, this should pull all module codes from the database
YEAR_CHOICES = (
    ('CM1101', 'CM1101'),
    ('CM1102', 'CM1102'),
    ('CM1103', 'CM1103')
)

class ReviewerManager(object):
    """
    Manager to assist in the creation of Reviewer models
    """
    def __init__(self):
        self.user_manager = UserManager()
        self.user_manager.model = User

    def create_new_reviewer(self, module_code, username, first_name, last_name,
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
        model = self.__create_model(module_code, user)

        # set the permissions
        user.is_reviewer = True
        user.save()
        return model

    def create_reviewer(self, module_code, user=None):
        """
        Method to create a reviewer from an existing user.
        Will configure the user permissions to be a year tutor.
        """
        if user is None:
            raise ValueError("Must select a user")

        # create the reviewer
        model = self.__create_model(module_code, user)
        if model is None:
            return None

        # update user permissions now the model has been created.
        user.is_reviewer = True
        user.save()
        return model

    def __create_model(self, module_code, user):
        """
        Private method to actually create the model.
        Could raise the Django IntegrityError if one
        to one relationship is violated.
        """
        if len(module_code) <= 0:
            raise ValueError("module_code must be a string greater than 0")
        try:
            reviewer = self.model.objects.create(
                module_code=module_code,
                reviewer_user=user
            )
            return tutor
        except IntegrityError:
            return None


class Reviewer(models.Model):
    """
    Model to represent reviewers
    """
    module_code = models.CharField(
        max_length=6,
        unique=True,
        choices=MODULE_CHOICES,
        default='CM1101'
    )

    reviewer_user = models.OneToOneField(User)

    objects = ReviewerManager()

    def __str__(self):
        return "{} {}".format(self.get_reviewer_name(), self.module_code)

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
        ordering = ['module_code']