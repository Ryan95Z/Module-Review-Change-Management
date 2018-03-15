from django.db import models
from core.models import User


class Watcher(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True
    )

    watching = models.ManyToManyField('core.Module')

    def watcher_username(self):
        return self.user.username

    def watcher_fullname(self):
        return self.user.get_full_name()
