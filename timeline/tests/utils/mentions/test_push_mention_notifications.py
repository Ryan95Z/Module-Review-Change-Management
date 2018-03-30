from core.models import Module
from timeline.models import Notification, TimelineEntry
from timeline.tests.common import BasicUserTestCase
from timeline.utils.mentions import push_mention_notifications


class TestPushMentionNotifications(BasicUserTestCase):
    """
    Test case for the push mention notifications util function
    """
    def setUp(self):
        super(TestPushMentionNotifications, self).setUp()
        self.func = push_mention_notifications
        self.model = Notification

        # test module
        self.module = Module.objects.create(
            module_code="CM2345",
            module_name="Test Module 2",
            module_credits="10",
            module_level="L1",
            semester="Autumn Semester",
            delivery_language="English",
            module_leader=self.user1
        )

        # test entry
        self.entry = TimelineEntry.objects.create(
            title="Test Changes",
            changes="Test changes to report",
            status="Draft",
            entry_type="Generic",
            module_code=self.module.module_code,
            object_id=self.module.module_code,
            content_object=self.module,
        )

    def test_push_mentions_notifications(self):
        """
        Test for executing the function as expected
        """
        # check with single mention
        sample = "@{} this is a test".format(self.user1.username)

        # expected notification content
        notice_txt_template = "{} mentioned you in a post for {}"

        notice_txt = notice_txt_template.format(
            self.admin.username,
            self.module.module_code
        )
        # test function
        output = self.func(sample, self.admin, self.entry)
        self.assertEquals(output, 1)

        # check a notification was added for user1
        notification = self.model.objects.get(recipient=self.user1)
        self.assertEquals(
            notification.recipient_username(),
            self.user1.username
        )
        self.assertEquals(notification.content, notice_txt)

        # delete notification to run next asserts
        notification.delete()

        # check with multiple mentions
        sample = "@{} @{} how about this".format(
            self.user1.username,
            self.user2.username
        )

        # test the function
        output = self.func(sample, self.admin, self.entry)
        self.assertEquals(output, 2)

        # check notifications were added,
        user1_notice = self.model.objects.get(recipient=self.user1)
        user2_notice = self.model.objects.get(recipient=self.user2)
        self.assertEquals(user1_notice.content, notice_txt)
        self.assertEquals(user2_notice.content, notice_txt)

    def test_push_mentions_notifications_author_mentioned(self):
        """
        Test to assert that if author is mentioned, it does
        not get a mention
        """
        author = self.user2
        notice_txt = "{} mentioned you in a post for {}".format(
            author.username,
            self.module.module_code
        )
        sample = "@{} this is amazing. I agree with myself. Me: @{}".format(
            self.user1.username,
            author.username
        )

        # test the function
        output = self.func(sample, author, self.entry)

        # has 1 less mentioned as the author will have been removed
        self.assertEquals(output, 1)

        # ensure there is no notification for author
        with self.assertRaises(self.model.DoesNotExist):
            self.model.objects.get(recipient=author)

        # assert notification for user1 was created
        notice = self.model.objects.get(recipient=self.user1)
        self.assertEquals(notice.content, notice_txt)

    def test_push_mentions_notifications_with_list(self):
        """
        Test push mentions notifications with list option
        """
        mentions = ["user1", "user2"]
        notice_txt = "{} mentioned you in a post for {}".format(
            self.admin.username,
            self.module.module_code
        )

        # test the list
        output = self.func(mentions, self.admin, self.entry)
        self.assertEquals(output, 2)

        # check a notification was added
        user1_notice = self.model.objects.get(recipient=self.user1)
        self.assertEquals(user1_notice.content, notice_txt)

    def test_push_mentions_invalid_mentions_type(self):
        """
        Test exceptions are raised when invalid mentions type
        is provided
        """

        # test with int
        with self.assertRaises(ValueError):
            self.func(12344, self.admin, self.entry)

        # test with dict
        with self.assertRaises(ValueError):
            self.func({1: 'uesr'}, self.admin, self.entry)

    def test_push_mentions_with_no_input(self):
        """
        Test that empty mentions gives 0 and does
        not process.
        """
        s1 = []
        s2 = ''

        # run the function
        o1 = self.func(s1, self.admin, self.entry)
        o2 = self.func(s2, self.admin, self.entry)

        # assert output true
        self.assertEquals(o1, 0)
        self.assertEquals(o2, 0)

    def test_push_mentions_invalid_author_entry(self):
        """
        Test to ensure invalid types are rejects for
        comment_author and entry.
        """
        # test with user param none
        with self.assertRaises(ValueError):
            self.func([], None, self.entry)

        # test with entry param none
        with self.assertRaises(ValueError):
            self.func([], self.user1, None)

        # test with both params none
        with self.assertRaises(ValueError):
            self.func([], None, None)

        # test with ints
        with self.assertRaises(ValueError):
            self.func([], 2, 3)

    def test_push_mentions_non_existent_user(self):
        """
        Test case to assert that non-existent users
        are not added to the database.
        """
        sample = "@ryan does not exist"
        output = self.func(sample, self.admin, self.entry)

        # check it still detects the user but does not
        # create a notification
        self.assertEquals(output, 1)

        # check all notifications. Should be zero as
        # none were added to the database
        notifications = self.model.objects.all()
        self.assertEquals(notifications.count(), 0)
