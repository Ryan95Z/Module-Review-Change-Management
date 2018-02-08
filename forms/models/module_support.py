from django.db import models
from core.models import Module
import json

class ModuleSupport(models.Model):
    """
    Model which represents the support information related to a module
    """
    support_id = models.AutoField(primary_key=True)
    lab_support_required = models.BooleanField(default=False)
    lab_support_skills = models.CharField(blank=True, max_length=500)
    lab_support_notes = models.TextField(blank=True, max_length=1000)
    tutorial_support_required = models.BooleanField(default=False)
    tutorial_support_skills = models.CharField(blank=True, max_length=500)
    tutorial_support_notes = models.TextField(blank=True, max_length=1000)
    module_code = models.OneToOneField(Module, on_delete=models.CASCADE)

    def __str__(self):
        return "Support information for {}".format(self.module_code)

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
