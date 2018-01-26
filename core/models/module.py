from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from .user import User


class Module(models.Model):
    module_code = models.CharField(max_length=6, primary_key=True)
    module_name = models.CharField(max_length=60, required=True)
    module_credits = models.IntegerField(validators=[
            MaxValueValidator(120),
            MinValueValidator(10)
    ])
    module_level = models.CharField()
    module_year = models.CharField()
    semester = models.CharField()
    deliveriy_language = models.CharField()
    module_leader = models.OneToOneField(User)
