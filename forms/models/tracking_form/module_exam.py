from django.db import models
from core.models import Module
from django.core.validators import MaxValueValidator

SEMESTER_OPTIONS = (
    ('Autumn Semester', 'Autumn Semester'),
    ('Spring Semester', 'Spring Semester'),
)

class ModuleExam(models.Model):
    """
    Model which represents the exam information related to a module
    """

    exam_id = models.AutoField(primary_key=True)
    exam_duration = models.PositiveSmallIntegerField()
    exam_weight = models.PositiveSmallIntegerField(validators=[MaxValueValidator(100)])
    exam_semester = models.CharField(choices=SEMESTER_OPTIONS, max_length=15)
    module_code = models.OneToOneField(Module, on_delete=models.CASCADE)

    def __str__(self):
        return "Exam for {}".format(self.module_code)
