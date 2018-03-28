from timeline.models import Discussion, TimelineEntry
from .base_timeline_model_testcase import BaseTimelineModelTestCase


class TestDiscussion(BaseTimelineModelTestCase):
    def setUp(self):
        super(TestDiscussion, self).setUp()
        self.model = Discussion
        self.basic_entry = TimelineEntry.objects.create(
            title="Test",
            changes="I am a test entry",
            status="Draft",
            entry_type="Generic",
            module_code=self.module.module_code,
            object_id=self.module.module_code,
            content_object=self.module,
            approved_by=self.user
        )

    def test_create_valid_model(self):
        """
        Test creation of valid models. One with no
        parent and another with.
        """

        # Test model creation without a parent
        comment = "Hello World, I am a test comment."
        discussion = self.model.objects.create(
            comment=comment,
            entry=self.basic_entry,
            author=self.user
        )

        # test properties
        self.assertEquals(discussion.comment, comment)
        self.assertEquals(discussion.entry, self.basic_entry)
        self.assertEquals(discussion.author, self.user)
        self.assertEquals(discussion.parent, None)

        # test methods
        self.assertEquals(discussion.author_username(), self.user.username)
        self.assertEquals(discussion.author_name(), self.user.get_full_name())

        # Test model creation with a parent
        comment = "I am a reply"
        reply_discussion = self.model.objects.create(
            comment=comment,
            entry=self.basic_entry,
            author=self.user,
            parent=discussion
        )

        # test properties
        self.assertEquals(reply_discussion.comment, comment)
        self.assertEquals(reply_discussion.entry, self.basic_entry)
        self.assertEquals(reply_discussion.author, self.user)
        self.assertEquals(reply_discussion.parent, discussion)

        # test methods
        self.assertEquals(
            reply_discussion.author_username(),
            self.user.username
        )

        self.assertEquals(
            reply_discussion.author_name(),
            self.user.get_full_name()
        )

    def test_model_cascade_entry_deleted(self):
        """
        Test model is deleted when the entry
        relating to it is deleted.
        """
        entry_id = self.basic_entry.pk
        comment = "Hello World, I am a test comment."
        discussion = self.model.objects.create(
            comment=comment,
            entry=self.basic_entry,
            author=self.user
        )

        discussion_id = discussion.pk

        # delete the entry
        self.basic_entry.delete()

        # check that the entry is removed
        with self.assertRaises(TimelineEntry.DoesNotExist):
            TimelineEntry.objects.get(pk=entry_id)

        # check that discusion is removed
        with self.assertRaises(self.model.DoesNotExist):
            self.model.objects.get(pk=discussion_id)

    def test_model_cascade_user_delete(self):
        """
        Test model is deleted when the user who
        created it is deleted.
        """
        comment = "Hello World, I am a test comment."
        discussion = self.model.objects.create(
            comment=comment,
            entry=self.basic_entry,
            author=self.user
        )

        discussion_id = discussion.pk

        # delete the user
        self.user.delete()

        # check that discusion is removed
        with self.assertRaises(self.model.DoesNotExist):
            self.model.objects.get(pk=discussion_id)
