from datetime import timedelta
from django.utils import timezone
from django.db import models
from core.models import User


class NotificationManager(models.Manager):
    def get_unseen_notifications(self, user):
        if not isinstance(user, str) and not isinstance(user, User):
            raise ValueError("user must be a username or core User object")

        if isinstance(user, str):
            user = self.__get_user(user)

        notifications = self.model.objects.filter(
            recipient=user.pk,
            seen=False
        )
        return notifications

    def get_all_notifications(self, user):
        if not isinstance(user, str) and not isinstance(user, User):
            raise ValueError("user must be a username or core User object")

        if isinstance(user, str):
            user = self.__get_user(user)

        # remove any old notifications
        self.get_unneeded_notifications(user.username)

        notifications = self.model.objects.filter(recipient=user.pk)
        return notifications

    def get_seen_notifications(self, username):
        user = User.objects.get(username=username)
        notifications = self.model.objects.filter(
            recipient=user.pk,
            seen=True
        )
        return notifications

    def __get_user(self, username):
        if username is None or len(username) < 1:
            raise ValueError("Username must not be none or an empty string")
        return User.objects.get(username=username)

    def get_unneeded_notifications(self, user):
        if not isinstance(user, str) and not isinstance(user, User):
            raise ValueError("user must be a username or core User object")

        if isinstance(user, str):
            user = self.__get_user(user)

        days_past = timedelta(days=5)
        today = timezone.now()
        difference_time = today - days_past

        return self.model.objects.filter(
            seen_at__lte=difference_time,
            seen=True,
            recipient=user
        )


class Notification(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    content = models.CharField(max_length=300)
    recipient = models.ForeignKey(User)
    seen = models.BooleanField(default=False)
    seen_at = models.DateTimeField(auto_now=True)
    link = models.CharField(max_length=100)

    objects = NotificationManager()

    def __str__(self):
        status = "Seen" if self.seen else "Not seen"
        return "{} ({})".format(self.content, status)

    def recipient_username(self):
        return self.recipient.username

    class Meta:
        ordering = ['-created']
