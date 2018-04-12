from .base_notice_test import BaseTestNotification
from django.urls import reverse
from timeline.models import TimelineEntry
from timeline.utils.notifications.notices import TLEntryNotice
from timeline.utils.notifications.helpers import WatcherWrapper


class TestTLEntryNotice(BaseTestNotification):
    """
    Test case for the TLEntryNotice object
    """
    def setUp(self):
        super(TestTLEntryNotice, self).setUp()
        self.notice = TLEntryNotice()

        # test timeline entry
        self.entry = TimelineEntry.objects.create(
            title="Changes to ",
            changes="Test Changes",
            status="Draft",
            entry_type="Draft",
            module_code=self.module.module_code,
            object_id=self.module.module_code,
            content_object=self.module,
            approved_by=self.module_leader
        )

        self.watcher = WatcherWrapper(self.user)
        self.watcher.add_module(self.module)

    def test_create_notification(self):
        """
        Test the creation of the notification
        """
        sample_data = {
            'entry': self.entry
        }

        # expected output
        expected_msg = self.notice.content_template.format(
            self.module.module_code
        )
        expected_link = reverse(self.notice.link_name, kwargs={
            'module_pk': self.module.module_code
        })

        # create the notification
        self.notice.create(**sample_data)

        # get the notification
        notification = self.model.objects.filter(recipient=self.user)
        self.assertEquals(notification.count(), 1)

        notice = notification.first()
        self.assertFalse(notice.seen)
        self.assertEquals(notice.content, expected_msg)
        self.assertEquals(notice.link, expected_link)
        self.assertEquals(notice.recipient, self.user)

    def test_create_notification_invalid_params(self):
        """
        Test exception is raised when invalid params are provided
        """
        # test with explict None in kwarg
        sample_data = {
            'entry': None
        }

        with self.assertRaises(ValueError):
            self.notice.create(**sample_data)

        # test with no kwargs
        with self.assertRaises(ValueError):
            self.notice.create()
