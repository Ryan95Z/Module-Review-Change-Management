from timeline.models import NotificationManager, Notification
from .base_timeline_model_testcase import BaseTimelineModelTestCase


class TestNotificationManager(BaseTimelineModelTestCase):
    """
    Test case for the NotificationManager
    """

    def setUp(self):
        super(TestNotificationManager, self).setUp()
        self.manager = NotificationManager()
        self.model = Notification
        self.manager.model = self.model

        # populate database with example notifications
        self.n1 = self.model.objects.create(
            content="Hello World!",
            recipient=self.user,
            link="/"
        )

        self.n2 = self.model.objects.create(
            content="Goodbye World!",
            recipient=self.user,
            link="/"
        )

        self.n3 = self.model.objects.create(
            content="No place like 127.0.0.1!",
            recipient=self.user,
            link="/"
        )

    def test_get_unseen_notifications(self):
        """
        Test case for get_unseen_notifications method
        """
        # test with user object
        user = self.user
        results = self.manager.get_unseen_notifications(user)

        # test it got three notifications
        self.assertEquals(results.count(), 3)

        # check all notifications are for this user and have
        # not been seen before
        for r in results:
            self.assertFalse(r.seen)
            self.assertEquals(r.recipient, self.user)

        # test with a string
        user = self.user.username
        results = self.manager.get_unseen_notifications(user)
        self.assertEquals(results.count(), 3)

        # check all notifications are for this user and have
        # not been seen before
        for r in results:
            self.assertFalse(r.seen)
            self.assertEquals(r.recipient, self.user)

    def test_get_unseen_notifications_invalid_params(self):
        """
        Test case to check that the method can handle invalid parameters
        """
        # array of invalid types
        invalid_users = [self.module, 1420030, 13.3333, "", "I am a fake user"]

        # execute each invalid param to check exception is triggered
        for invalid in invalid_users:
            with self.assertRaises(ValueError):
                self.manager.get_unseen_notifications(invalid)

    def test_get_all_notifications(self):
        """
        Test case for get_all_notifications method
        """
        # add seen notification
        self.model.objects.create(
            content="It’s not a bug – it’s an undocumented feature!",
            recipient=self.user,
            link="/",
            seen=True,
        )

        # test with string username and user object
        user = [self.user, self.user.username]
        for u in user:
            results = self.manager.get_all_notifications(u)
            # check it found the 4 notifications
            self.assertEquals(results.count(), 4)

            seen = 0
            unseen = 0
            expected_seen = 1
            expected_unseen = 3

            # count the seen vs unseen notifications
            for r in results:
                self.assertEquals(r.recipient, self.user)
                if r.seen:
                    seen += 1
                else:
                    unseen += 1

            # check that it go the different types
            self.assertEquals(seen, expected_seen)
            self.assertEquals(unseen, expected_unseen)

    def test_get_all_notifications_invalid_params(self):
        """
        Test case to check that the method can handle invalid parameters
        """
        # array of invalid types
        invalid_users = [self.module, 1420030, 13.3333, "", "I am a fake user"]

        # execute each invalid param to check exception is triggered
        for invalid in invalid_users:
            with self.assertRaises(ValueError):
                self.manager.get_all_notifications(invalid)

    def test_get_seen_notifications(self):
        """
        Test case for get_seen_notifications method
        """
        # add seen notification
        self.model.objects.create(
            content="Deleted code is debugged code.",
            recipient=self.user,
            link="/",
            seen=True,
        )

        # test with string username and user object
        user = [self.user, self.user.username]

        for u in user:
            results = self.manager.get_seen_notifications(u)
            self.assertEquals(results.count(), 1)

            for r in results:
                # check it is for this user and iis seen
                self.assertEquals(r.recipient, self.user)
                self.assertTrue(r.seen)

    def test_get_seen_notifications_invalid_params(self):
        """
        Test case to check that the method can handle invalid parameters
        """
        # array of invalid types
        invalid_users = [self.module, 1420030, 13.3333, "", "I am a fake user"]

        # execute each invalid param to check exception is triggered
        for invalid in invalid_users:
            with self.assertRaises(ValueError):
                self.manager.get_seen_notifications(invalid)

    def test_get_unneeded_notifications(self):
        """
        Test case for get_unneeded_notifications method
        """
        user = [self.user, self.user.username]
        for u in user:
            results = self.manager.get_unneeded_notifications(u)
            self.assertEquals(results.count(), 0)

    def test_get_unneeded_notifications_invalid_params(self):
        """
        Test case to check that the method can handle invalid parameters
        """
        # array of invalid types
        invalid_users = [self.module, 1420030, 13.3333, "", "I am a fake user"]

        # execute each invalid param to check exception is triggered
        for invalid in invalid_users:
            with self.assertRaises(ValueError):
                self.manager.get_unneeded_notifications(invalid)


class TestNotification(BaseTimelineModelTestCase):
    """
    Test case for the Notification model
    """
    def setUp(self):
        super(TestNotification, self).setUp()
        self.model = Notification

    def test_create_valid_notification(self):
        """
        Test creation of a valid model
        """
        msg = "A good programmer is someone who always looks both ways before \
                crossing a one-way street."
        link = "/"

        # create notification
        notice = self.model.objects.create(
            content=msg,
            recipient=self.user,
            link=link,
        )

        # test attributes
        self.assertEquals(notice.content, msg)
        self.assertEquals(notice.recipient, self.user)
        self.assertEquals(notice.link, link)
        self.assertFalse(notice.seen)

        # test method
        self.assertEquals(notice.recipient_username(), self.user.username)
