from django.db import models
from django.core.validators import MaxValueValidator
from timeline.models.integrate.entry import TLEntry
from django.core.exceptions import ObjectDoesNotExist

from core.models import Module

HAND_OUT_IN_OPTIONS = (
    ('1A', 'Autumn Week 1'),
    ('2A', 'Autumn Week 2'),
    ('3A', 'Autumn Week 3'),
    ('4A', 'Autumn Week 4'),
    ('5A', 'Autumn Week 5'),
    ('6A', 'Autumn Week 6'),
    ('7A', 'Autumn Week 7'),
    ('8A', 'Autumn Week 8'),
    ('9A', 'Autumn Week 9'),
    ('10A', 'Autumn Week 10'),
    ('11A', 'Autumn Week 11'),
    ('1S', 'Spring Week 1'),
    ('2S', 'Spring Week 2'),
    ('3S', 'Spring Week 3'),
    ('4S', 'Spring Week 4'),
    ('5S', 'Spring Week 5'),
    ('6S', 'Spring Week 6'),
    ('7S', 'Spring Week 7'),
    ('8S', 'Spring Week 8'),
    ('9S', 'Spring Week 9'),
    ('10S', 'Spring Week 10'),
    ('11S', 'Spring Week 11'),
)

SEMESTER_OPTIONS = (
    ('Autumn Semester', 'Autumn Semester'),
    ('Spring Semester', 'Spring Semester'),
)

class ModuleAssessmentManager(models.Manager):
    """
    Manager for the ModuleAssessment model
    """
    def get_current_assessments(self, module):
        current_assessments = self.filter(module=module, current_flag=True)
        if current_assessments:
            return current_assessments
        else:
            raise ObjectDoesNotExist('No assessments with the current_flag exist')


class ModuleAssessment(TLEntry):
    """
    Model which represents the assessment details of a module
    """

    assessment_id = models.AutoField(primary_key=True)
    assessment_title = models.CharField(max_length=100, verbose_name="Title")
    assessment_type = models.CharField(max_length=50, verbose_name="Type")
    assessment_weight = models.PositiveSmallIntegerField(validators=[MaxValueValidator(100)], verbose_name="Weighting")
    assessment_duration = models.PositiveSmallIntegerField(verbose_name="Duration (hours)")
    assessment_hand_out = models.CharField(choices=HAND_OUT_IN_OPTIONS, max_length=15, verbose_name="Hand out week")
    assessment_hand_in = models.CharField(choices=HAND_OUT_IN_OPTIONS, max_length=15, verbose_name="Hand in week")
    assessment_semester = models.CharField(blank=True, choices=SEMESTER_OPTIONS, max_length=15, verbose_name="Semester")
    learning_outcomes_covered = models.CharField(max_length=500, verbose_name="Learning Outcomes Covered")

    archive_flag = models.BooleanField(default=False)
    staging_flag = models.BooleanField(default=False)
    current_flag = models.BooleanField(default=False)
    version_number = models.IntegerField(default=1)
    copy_number = models.IntegerField(default=1)

    objects = ModuleAssessmentManager()

    def __str__(self):
        return "{} for {}".format(self.assessment_title, self.module)

    def title(self):
        return "Assessment {}".format(self.assessment_title)