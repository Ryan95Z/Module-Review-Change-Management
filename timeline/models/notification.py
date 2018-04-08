from datetime import timedelta
from django.utils import timezone
from django.db import models
from core.models import User


class NotificationManager(models.Manager):
    """
    Manager for notifcation object. Provides helpful methods
    to get certain types of notifications out.
    """
    def get_unseen_notifications(self, user):
        """
        Get all notifications for user that have not been seen

        Arguments:
            user    A string of the username or a User object

        Return:
            QueryList of Notifications
        """
        if not isinstance(user, str) and not isinstance(user, User):
            raise ValueError("user must be a username or core User object")

        if isinstance(user, str):
            user = self.__get_user(user)

        if user is None:
            raise ValueError(
                "user should not be None. This username does not exist")

        notifications = self.model.objects.filter(
            recipient=user.pk,
            seen=False
        )
        return notifications

    def get_all_notifications(self, user):
        """
        Gets all the notifications for a user. This include ones
        they have seen and have not seen yet.

        Arguments:
            user    A string of the username or a User object

        Return:
            QueryList of Notifications
        """
        if not isinstance(user, str) and not isinstance(user, User):
            raise ValueError("user must be a username or core User object")

        if isinstance(user, str):
            user = self.__get_user(user)

        if user is None:
            raise ValueError(
                "user should not be None. This username does not exist")

        # remove any old notifications
        self.get_unneeded_notifications(user.username).delete()

        notifications = self.model.objects.filter(recipient=user.pk)
        return notifications

    def get_seen_notifications(self, user):
        """
        Gets all notifications that have been seen by user.

        Arguments:
            user    A string of the username or a User object

        Return:
            QueryList of Notifications
        """
        if not isinstance(user, str) and not isinstance(user, User):
            raise ValueError("user must be a username or core User object")

        if isinstance(user, str):
            user = self.__get_user(user)

        if user is None:
            raise ValueError(
                "user should not be None. This username does not exist")

        notifications = self.model.objects.filter(
            recipient=user.pk,
            seen=True
        )
        return notifications

    def get_unneeded_notifications(self, user):
        """
        Removes all old seen notifications that are no longer relevant
        to the user.

        Arguments:
            user    A string of the username or a User object

        Return:
            QueryList of Notifications
        """
        if not isinstance(user, str) and not isinstance(user, User):
            raise ValueError("user must be a username or core User object")

        if isinstance(user, str):
            user = self.__get_user(user)

        if user is None:
            raise ValueError(
                "user should not be None. This username does not exist")

        days_past = timedelta(days=5)
        today = timezone.now()

        # time difference between 5 days and today
        difference_time = today - days_past

        return self.model.objects.filter(
            seen_at__lte=difference_time,
            seen=True,
            recipient=user
        )

    #############################
    # Private methods
    ##############################
    def __get_user(self, username):
        """
        Gets the user object when a username is provided

        Arguments:
            username        string of username

        Return:
            User object if user exists
        """
        if username is None or len(username) < 1:
            raise ValueError("Username must not be none or an empty string")
        try:
            return User.objects.get(username=username)
        except User.DoesNotExist:
            return None


class Notification(models.Model):
    """
    Model to represent a notification
    """
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
        """
        Method to recipient's username
        """
        return self.recipient.username

    class Meta:
        ordering = ['-created']
