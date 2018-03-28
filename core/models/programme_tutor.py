from django.db import models
from django.db import IntegrityError
from core.models import Module, User, UserManager

# choices for tutor_year field in YearTutor model
YEAR_CHOICES = (
    ('Year 1', 'Year 1'),
    ('Year 2', 'Year 2'),
    ('Year 3', 'Year 3'),
    ('MSC', 'MSC')
)


class ProgrammeTutorManager(object):
    """
    Manager to assit in the creation of Programme Tutors models
    """
    def __init__(self):
        self.user_manager = UserManager()
        self.user_manager.model = User

    def create_new_tutor(self, programme_name, tutor_year, username,
                         first_name, last_name, email, password=None):

        """
        Create a new user with all of the expected parameters
        as the user manager for the programme tutor.
        """

        # create the user to become a programme tutor
        user = self.user_manager.create_user(
            username=username,
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=password
        )

        # create the year tutor model
        model = self.__create_model(programme_name, tutor_year, user)

        # set the permissions now the model is created
        user.is_year_tutor = True
        user.save()
        return model

    def create_tutor(self, programme_name, tutor_year, user):
        """
        Method to create a programme tutor on an existing user.
        Will configure the user permissions to be a year tutor.
        """
        if user is None:
            raise ValueError("User must not be None")

        # create the year tutor
        model = self.__create_model(programme_name, tutor_year, user)
        if model is None:
            return None

        # update user permissions now the model has been created.
        user.is_year_tutor = True
        user.save()
        return model

    def __create_model(self, programme_name, tutor_year, user):
        """
        Private method to actually create the model.
        Could raise the Django IntegrityError if one
        to one relationship is violated.
        """

        # if the programme name and the tutor year are blank
        if len(programme_name) <= 0 or len(tutor_year) <= 0:
            raise ValueError(
                "Programme name and tutor year cannot be empty strings")
        try:
            tutor = self.model.objects.create(
                programme_name=programme_name,
                tutor_year=tutor_year,
                programme_tutor_user=user
            )
            return tutor
        except IntegrityError:
            return None


class ProgrammeTutor(models.Model):
    """
    Model to represent the programme tutors
    """
    programme_name = models.CharField(
        max_length=30,
        default=""
    )

    tutor_year = models.CharField(
        max_length=7,
        choices=YEAR_CHOICES,
        default='year 1'
    )

    programme_tutor_user = models.OneToOneField(User)

    modules = models.ManyToManyField(Module)

    objects = ProgrammeTutorManager()

    def __str__(self):
        return "{} {}: {}".format(
            self.programme_name,
            self.get_tutor_name(),
            self.tutor_year
        )

    def get_tutor_name(self):
        """
        Method to get the tutor's fullname
        """
        return self.programme_tutor_user.get_full_name()

    def get_tutor_username(self):
        """
        Method to get the username of the tutor
        """
        return self.programme_tutor_user.username

    def get_tutor_id(self):
        """
        Method to return the id of the user assigned
        to the year.
        """
        return self.programme_tutor_user.id

    class Meta:
        ordering = ['tutor_year']
        unique_together = ('programme_name', 'tutor_year',)
