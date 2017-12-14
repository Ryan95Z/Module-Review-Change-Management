from django.db import models
from django.db import IntegrityError
from .user import User, UserManager

YEAR_CHOICES = (
    ('year 1', 'Year 1'),
    ('year 2', 'Year 2'),
    ('year 3', 'Year 3'),
    ('msc', 'MSC')
)


class YearTutorManager(object):
    def __init__(self):
        self.model = YearTutor
        self.user_manager = UserManager

    def create_new_tutor(self, tutor_year, username, first_name,
                         last_name, email, password=None):

        """
        Create a new user with all of the expected parameters
        as the user manager. This will then be used to create
        link the tutor to the model.
        """

        # create the user to become a year tutor
        user = self.user_manager.create_user(
            username=username,
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=password
        )

        # set the permissions
        user.is_year_tutor = True
        user.save()

        # create the year tutor model
        return self.__create_model(tutor_year, user)

    def create_tutor(self, tutor_year, user=None):
        """
        Method to create a year tutor on an existing user.
        Will configure the user permissions to be a year tutor.
        """
        if user is None:
            raise ValueError("User must not be none")

        # update user permissions
        user.is_year_tutor = True
        user.save()

        # create the year tutor
        return self.__create_model(tutor_year, user)

    def __create_model(self, tutor_year, user):
        """
        Private method to actually create the model.
        Could raise the Django IntegrityError if one
        to one relationship is violated.
        """
        try:
            tutor = self.model.objects.create(
                tutor_year=tutor_year,
                year_tutor_user=user
            )
            return tutor
        except IntegrityError:
            return None


class YearTutor(models.Model):
    """
    Model to represent the year tutors
    """
    tutor_year = models.CharField(
        max_length=7,
        choices=YEAR_CHOICES,
        default='year 1'
    )

    year_tutor_user = models.OneToOneField(User)

    def __str__(self):
        return "{} {}".format(self.get_tutor_name(), self.tutor_year)

    def get_tutor_name(self):
        """
        Method to get the tutor's fullname
        """
        return self.year_tutor_user.get_full_name()

    def get_tutor_username(self):
        """
        Method to get the username of the tutor
        """
        return self.year_tutor_user.username

    def get_tutor_id(self):
        """
        Method to return the id of the user assigned
        to the year.
        """
        return self.year_tutor_user.id
