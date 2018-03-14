from django.db import models
from core.models import User


class NotificationManager(models.Manager):
    def get_unseen_notifications(self, username):
        notifications = self.model.objects.filter(seen=False)
        return notifications


class Notification(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    content = models.CharField(max_length=300)
    recipient = models.ForeignKey(User)
    seen = models.BooleanField(default=False)

    objects = NotificationManager()

    def __str__(self):
        status = "seen" if self.seen else "not seen"
        return "{}| {} for {}".format(
                status, self.id, self.recipient_username())

    def recipient_username(self):
        return self.recipient.username
