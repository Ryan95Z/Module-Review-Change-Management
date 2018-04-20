from .base_notice_test import BaseTestNotification
from django.urls import reverse
from timeline.models import Discussion, TimelineEntry
from timeline.utils.notifications.notices import DiscussionNotice
from timeline.utils.notifications.helpers import WatcherWrapper


class TestDiscussionNotice(BaseTestNotification):
    """
    Test case for the DiscussionNotice object
    """
    def setUp(self):
        super(TestDiscussionNotice, self).setUp()
        self.notice = DiscussionNotice()

        # create test timeline entry
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

        # create a test disucssions
        self.discussion = Discussion.objects.create(
            comment="This is a new comment",
            entry=self.entry,
            author=self.module_leader,
        )

        self.watcher = WatcherWrapper(self.user)
        self.watcher.add_module(self.module)

    def test_create_notification(self):
        """
        Test case for creating a notification
        """
        sample_data = {
            'discussion': self.discussion,
            'user': self.module_leader
        }

        # expected outputs
        expected_msg = self.notice.content_template.format(
            self.module_leader.username,
            self.module.module_code
        )

        expected_link = reverse(self.notice.link_name, kwargs={
            'module_pk': self.module.module_code,
            'pk': self.discussion.entry.pk
        })

        # create the notification from object
        self.notice.create(**sample_data)

        # Test the notification was created as expected
        notification = self.model.objects.filter(recipient=self.user).first()
        self.assertFalse(notification.seen)
        self.assertEquals(notification.content, expected_msg)
        self.assertEquals(notification.recipient, self.user)
        self.assertEquals(notification.link, expected_link)

    def test_create_notification_author_writes_on_comment(self):
        """
        Test that a notification is not created when the author
        of the discussion writes it.
        """
        # add the module to the module leader
        watcher = WatcherWrapper(self.module_leader)
        watcher.add_module(self.module)

        sample_data = {
            'discussion': self.discussion,
            'user': self.module_leader
        }

        # create the notification
        self.notice.create(**sample_data)

        # assert that the notification is not created for the module
        # leader, who created the discussion as well as added the comment.
        notifications = self.model.objects.filter(recipient=self.module_leader)
        self.assertEquals(notifications.count(), 0)

        # assert it was still created for the other user who is
        # watching the module.
        notifications = self.model.objects.filter(recipient=self.user)
        self.assertEquals(notifications.count(), 1)

    def test_create_notification_null_params(self):
        """
        Test case to ensure exception is raised is None
        params to param or kwarg is not provided.
        """

        sample_data = {
            'discussion': self.discussion
        }

        # test with missing kwarg user
        with self.assertRaises(ValueError):
            self.notice.create(**sample_data)

        # test with None kwarg
        sample_data = {
            'discussion': None,
            'user': self.user
        }

        with self.assertRaises(ValueError):
            self.notice.create(**sample_data)

        # test with both None:
        with self.assertRaises(ValueError):
            self.notice.create()
