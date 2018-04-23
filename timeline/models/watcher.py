from django.db import models
from core.models import User


class Watcher(models.Model):
    """
    Model to provide a link between which users should
    receive notifications for particular models
    """
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True
    )

    # the modules thet are assigned to a user
    watching = models.ManyToManyField('core.Module')

    def watcher_username(self):
        """
        Gets user's username
        """
        return self.user.username

    def watcher_fullname(self):
        """
        Gets user's fullname
        """
        return self.user.get_full_name()
