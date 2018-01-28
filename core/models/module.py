from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from .user import User

DELIVERY_LANGUAGES = (
    ('cy', 'Welsh'),
    ('en', 'English')
)

SEMESTER_OPTIONS = (
    ('AS', 'Autumn Semester'),
    ('SS', 'Sprint Semester'),
    ('DS', 'Double Semester')
)


class Module(models.Model):
    """
    Model for representing a module
    """
    module_code = models.CharField(max_length=6, primary_key=True)
    module_name = models.CharField(max_length=60)
    module_credits = models.IntegerField(validators=[
            MaxValueValidator(120),
            MinValueValidator(10)
    ])
    module_level = models.CharField(max_length=10)
    module_year = models.CharField(max_length=15)

    semester = models.CharField(
        max_length=15,
        choices=SEMESTER_OPTIONS
    )

    delivery_language = models.CharField(
        max_length=10,
        choices=DELIVERY_LANGUAGES
    )
    module_leader = models.ForeignKey(User)

    def __str__(self):
        return "{}: {}".format(self.module_code, self.module_name)

    def module_leader_name(self):
        """
        Return the module leader's full name
        """
        return self.module_leader.get_full_name()

    def module_leader_username(self):
        """
        Return the module leader's username
        """
        return self.module_leader.username

    def module_leader_id(self):
        """
        Return the module leader's db id
        """
        return self.module_leader.id

    class Meta:
        ordering = ['module_code']
