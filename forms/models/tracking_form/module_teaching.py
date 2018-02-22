from django.db import models
from core.models import Module

class ModuleTeaching(models.Model):
    """
    Model which represents teaching information related to a module
    """
    teaching_id = models.AutoField(primary_key=True)
    teaching_lectures = models.PositiveSmallIntegerField(default=0, verbose_name="Classroom-based lectures")
    teaching_tutorials = models.PositiveSmallIntegerField(default=0, verbose_name="Classroom-based seminars and/or tutorials")
    teaching_online = models.PositiveSmallIntegerField(default=0, verbose_name="Scheduled online activities (Online versions on the above)")
    teaching_practical_workshops = models.PositiveSmallIntegerField(default=0, verbose_name="Practical classes and workshops")
    teaching_supervised_time = models.PositiveSmallIntegerField(default=0, verbose_name="Supervised time in studio/laboratory/workshop")
    teaching_fieldworks = models.PositiveSmallIntegerField(default=0, verbose_name="Fieldwork")
    teaching_external_visits = models.PositiveSmallIntegerField(default=0, verbose_name="External Visits")
    teaching_schedule_assessment = models.PositiveSmallIntegerField(default=0, verbose_name="Scheduled examination/assessment")
    teaching_placement = models.PositiveSmallIntegerField(default=0, verbose_name="Placement")
    module_code = models.OneToOneField(Module, on_delete=models.CASCADE)

    def __str__(self):
        return "Teaching hours for {}".format(self.module_code)

    def total_teaching_hours(self):
        """
        Return the total teaching hours for the given module
        """

        return sum([
            self.teaching_lectures,
            self.teaching_tutorials,
            self.teaching_online,
            self.teaching_practical_workshops,
            self.teaching_supervised_time,
            self.teaching_fieldworks,
            self.teaching_external_visits,
            self.teaching_schedule_assessment,
            self.teaching_placement
        ])
