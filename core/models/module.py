from django.db import models
from django.db.utils import IntegrityError
from django.core.validators import MaxValueValidator, MinValueValidator
from core.models import User

from timeline.models.integrate import BaseTimelineNode

DELIVERY_LANGUAGES = (
    ('Welsh', 'Welsh'),
    ('English', 'English')
)

SEMESTER_OPTIONS = (
    ('Autumn Semester', 'Autumn Semester'),
    ('Spring Semester', 'Spring Semester'),
    ('Double Semester', 'Double Semester')
)


class ModuleManager(models.Manager):
    """
    Manager for the module model
    """

    def create_module(self, module_code, module_name, module_credits,
                      module_level, semester, delivery_language,
                      module_leader):
        """
        Method to create a module model
        """
        # ensure that module leader is not None
        if module_leader is None:
            raise IntegrityError("Module Leader cannot be None")

        # check that credits do not exceed ranges
        if module_credits < 10 or module_credits > 120:
            raise ValueError(
                "Module credits must be between 10 to 120 credits"
            )

        model = self.model.objects.create(
            module_code=module_code,
            module_name=module_name,
            module_credits=module_credits,
            module_level=module_level,
            semester=semester,
            delivery_language=delivery_language,
            module_leader=module_leader
        )

        module_leader.is_module_leader = True
        module_leader.save()
        return model


class Module(BaseTimelineNode):
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

    semester = models.CharField(
        max_length=15,
        choices=SEMESTER_OPTIONS
    )

    delivery_language = models.CharField(
        max_length=10,
        choices=DELIVERY_LANGUAGES
    )
    module_leader = models.ForeignKey(User)

    objects = ModuleManager()

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

    def title(self):
        """
        Override from BaseTimelineNode to define
        title that will be used on timeline.
        """
        return self.module_code

    class Meta:
        ordering = ['module_code']
