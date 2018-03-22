import math
from datetime import datetime
from django.db import models
from django.utils.dateformat import format
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

    def remove_old_notifications(self, username):
        max_days = 10
        items_deleted = False
        notifications = self.get_seen_notifications(username)

        # current time
        now = datetime.now()
        now_timestamp = format(now, u'U')

        # loop through all notifications and remove
        # any that are older than 10 days.
        for n in notifications:
            created_timestamp = format(n.seen_at, u'U')

            # calculates the number of days have passed between
            # now and the time the notification was created.
            # formula to calculate difference in days was found here:
            # https://stackoverflow.com/questions/4079814/finding-days-between-2-unix-timestamps-in-php
            diff = ((int(now_timestamp) - int(created_timestamp)) / 86400)
            days = math.floor(diff)

            # if the day has passed
            if days >= max_days:
                items_deleted = True
                n.delete()
        return items_deleted

    def __get_user(self, username):
        if username is None or len(username) < 1:
            raise ValueError("Username must not be none or an empty string")
        return User.objects.get(username=username)


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
