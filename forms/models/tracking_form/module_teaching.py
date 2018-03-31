from django.db import models
from timeline.models.integrate.entry import TLEntry

from core.models import Module


class ModuleTeaching(TLEntry):
    """
    Model which represents teaching information related to a module
    """
    teaching_id = models.AutoField(primary_key=True)
    teaching_lectures = models.PositiveSmallIntegerField(verbose_name="Classroom-based lectures")
    teaching_tutorials = models.PositiveSmallIntegerField(verbose_name="Classroom-based seminars and/or tutorials")
    teaching_online = models.PositiveSmallIntegerField(verbose_name="Scheduled online activities (Online versions on the above)")
    teaching_practical_workshops = models.PositiveSmallIntegerField(verbose_name="Practical classes and workshops")
    teaching_supervised_time = models.PositiveSmallIntegerField(verbose_name="Supervised time in studio/laboratory/workshop")
    teaching_fieldworks = models.PositiveSmallIntegerField(verbose_name="Fieldwork")
    teaching_external_visits = models.PositiveSmallIntegerField(verbose_name="External Visits")
    teaching_schedule_assessment = models.PositiveSmallIntegerField(verbose_name="Scheduled examination/assessment")
    teaching_placement = models.PositiveSmallIntegerField(verbose_name="Placement")

    archive_flag = models.BooleanField(default=False)
    staging_flag = models.BooleanField(default=False)
    current_flag = models.BooleanField(default=False)
    version_number = models.IntegerField(default=1)
    copy_number = models.IntegerField(default=1)


    def __str__(self):
        return "Teaching hours for {}".format(self.module)

    def title(self):
        return "Module Teaching"

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
