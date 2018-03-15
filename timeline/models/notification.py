from django.db import models
from core.models import User


class NotificationManager(models.Manager):
    def get_unseen_notifications(self, username):
        user = User.objects.get(username=username)
        notifications = self.model.objects.filter(
            recipient=user.pk,
            seen=False
        )
        return notifications

    def get_all_notifications(self, username):
        user = User.objects.get(username=username)
        notifications = self.model.objects.filter(recipient=user.pk)
        return notifications

    def get_seen_notifications(self, username):
        user = User.objects.get(username=username)
        notifications = self.model.objects.filter(
            recipient=user.pk,
            seen=True
        )
        return notifications


class Notification(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    content = models.CharField(max_length=300)
    recipient = models.ForeignKey(User)
    seen = models.BooleanField(default=False)
    link = models.CharField(max_length=100)

    objects = NotificationManager()

    def __str__(self):
        status = "Seen" if self.seen else "Not seen"
        return "{} ({})".format(self.content, status)

    def recipient_username(self):
        return self.recipient.username
