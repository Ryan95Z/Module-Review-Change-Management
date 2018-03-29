from django.db import models
from timeline.register import timeline_register
from timeline.models.integrate.entry import TLEntry

from core.models import Module
import json

# @timeline_register
class ModuleSupport(TLEntry):
    """
    Model which represents the support information related to a module
    """
    support_id = models.AutoField(primary_key=True)
    lab_support_required = models.BooleanField(default=False, 
        verbose_name="Do you require PhD student support for your labs?")
    lab_support_skills = models.CharField(blank=True, max_length=500, 
        verbose_name="What skills will lab tutors require?")
    lab_support_notes = models.TextField(blank=True, max_length=1000, verbose_name="Notes")
    tutorial_support_required = models.BooleanField(default=False, 
        verbose_name="Do you require Phd student support for your tutorials?")
    tutorial_support_skills = models.CharField(blank=True, max_length=500, 
        verbose_name="What skills will the tutors require?")
    tutorial_support_notes = models.TextField(blank=True, max_length=1000, verbose_name="Notes")

    archive_flag = models.BooleanField(default=False)
    staging_flag = models.BooleanField(default=False)
    current_flag = models.BooleanField(default=False)

    def __str__(self):
        return "Support information for {}".format(self.module)

    def title(self):
        return "Module Support"

    def lab_support_skills_json(self):
        """
        Tries to convert the lab support skills to json and return them
        """
        return __convert_to_json(self.lab_support_skills)

    def tutorial_support_skills_json(self):
        """
        Tries to convert the tutorial support skills to json and return them
        """
        return __convert_to_json(self.tutorial_support_skills)
    
    def __convert_to_json(self, json):
        """
        Private method which attempts to convert a given string into json.
        If it fails it returns nothing
        """
        try:
            return json.loads(json)
        except ValueError:
            return None
