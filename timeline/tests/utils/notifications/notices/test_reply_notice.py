from .base_notice_test import BaseTestNotification
from django.urls import reverse
from timeline.models import Discussion, TimelineEntry
from timeline.utils.notifications.notices import ReplyNotice


class TestReplyNotice(BaseTestNotification):
    """
    Test case for the ReplyNotice object
    """
    def setUp(self):
        super(TestReplyNotice, self).setUp()
        self.notice = ReplyNotice()

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

        self.reply = Discussion.objects.create(
            comment="I am a reply",
            entry=self.entry,
            author=self.user,
            parent=self.discussion
        )

    def test_create_notification(self):
        """
        Test the creation of a reply notification
        """

        sample_data = {
            'discussion': self.reply,
            'user': self.user,
            'parent': self.discussion
        }

        expected_msg = self.notice.content_template.format(self.user.username)
        expected_link = reverse(self.notice.link_name, kwargs={
            'module_pk': self.module.module_code,
            'pk': self.entry.pk
        })

        # create the notification
        self.notice.create(**sample_data)

        # get and test the notification
        notification = self.model.objects.filter(recipient=self.module_leader)
        self.assertEqual(notification.count(), 1)

        notification = notification.first()
        self.assertFalse(notification.seen)
        self.assertEqual(notification.content, expected_msg)
        self.assertEqual(notification.link, expected_link)
        self.assertEqual(notification.recipient, self.module_leader)

    def test_create_notification_reply_from_comment_owner(self):
        """
        Test for asserting that user who owns main comment and reply
        does not get a notification
        """

        # create a reply with the same user that
        # wrote the parent comment
        reply = Discussion.objects.create(
            comment="I am replying to my own comment",
            entry=self.entry,
            author=self.module_leader,
            parent=self.discussion
        )

        sample_data = {
            'discussion': reply,
            'user': self.module_leader,
            'parent': self.discussion
        }

        # create the notification
        self.notice.create(**sample_data)

        # assert it was not created
        notifications = self.model.objects.filter(recipient=self.module_leader)
        self.assertEqual(notifications.count(), 0)

    def test_create_notification_invalid_params(self):
        """
        Test that exceptions are raised if keywords are not provided.
        """
        # discussion keyword missing
        sample_data = {
            'user': self.module_leader,
            'parent': self.discussion
        }
        with self.assertRaises(ValueError):
            self.notice.create(**sample_data)

        # test with explict none value for user
        sample_data = {
            'discussion': self.reply,
            'user': None,
            'parent': self.discussion
        }
        with self.assertRaises(ValueError):
            self.notice.create(**sample_data)

        # test with parent missing
        sample_data = {
            'discussion': self.reply,
            'user': self.user,
        }
        with self.assertRaises(ValueError):
            self.notice.create(**sample_data)

        # test with no keywords
        with self.assertRaises(ValueError):
            self.notice.create()
