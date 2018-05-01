from timeline.models import Notification
from timeline.utils.notifications.factory import NotificationFactory
from timeline.utils.notifications.notices import ModuleLeaderNotice
from core.tests.common_test_utils import LoggedInTestCase, ModuleTestCase


class TestNotificationFactory(LoggedInTestCase, ModuleTestCase):
    """
    Test case for the Notification Factory object
    """
    def setUp(self):
        super(TestNotificationFactory, self).setUp()
        self.factory = NotificationFactory
        self.test_notice = ModuleLeaderNotice

        self.notice_data = {
            'module_code': self.module.module_code,
            'module_leader': self.module_leader
        }

        self.alis = "ModuleLeader"

    def test_register_notification(self):
        """
        Test the registering of a new object
        """
        self.factory.register(self.test_notice, self.alis)
        self.assertEqual(len(self.factory.factories), 8)

        # check that it is registered
        instances = self.factory.assigned_instances()
        self.assertTrue(self.alis in instances)
        self.assertEqual(len(instances), 8)

    def test_get_notification_object(self):
        """
        Test the factory to get the object
        """
        self.factory.register(self.test_notice, self.alis)
        obj = self.factory.get(self.alis)

        # test it is the same type
        self.assertEqual(obj.__class__, self.test_notice)

    def test_making_a_notification(self):
        """
        Test the factory in making a new notification to the database
        """
        self.factory.register(self.test_notice, self.alis)

        # make the notification
        self.factory.makeNotification(self.alis, **self.notice_data)

        notice = self.test_notice()
        expected_message = notice.content_template.format(
            self.notice_data['module_code']
        )

        # get the notification
        notice = Notification.objects.all().first()
        self.assertEqual(notice.content, expected_message)
        self.assertEqual(
            notice.recipient_username(),
            self.module_leader.username
        )

        self.assertEqual(notice.recipient, self.module_leader)
        self.assertFalse(notice.seen)

    def test_invalid_register_params(self):
        """
        Test case for invalid params of register method
        """

        # fake class
        class FakeNotice(object):
            def create(self, **kwargs):
                return 1

        # test params that will be looped through
        test_params = {
            1: (self.test_notice, ""),
            2: (None, "test"),
            3: (FakeNotice, "test"),
        }

        for key, params in test_params.items():
            with self.assertRaises(ValueError):
                self.factory.register(params[0], params[1])

    def test_invalid_methods_params(self):
        """
        Test case for ensuring exceptions are triggered
        for other parameters
        """

        # test the get method
        with self.assertRaises(ValueError):
            self.factory.get("")

        # test make notification
        with self.assertRaises(ValueError):
            self.factory.makeNotification("", test=True)
