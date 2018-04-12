from django.core.urlresolvers import reverse
from timeline.models import TimelineEntry, Discussion
from timeline.tests.views.base_timeline_view_test_case import BaseTimelineViewTestCase


class TestDiscussionsDeleteView(BaseTimelineViewTestCase):
    def setUp(self):
        super(TestDiscussionsDeleteView, self).setUp()

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

        self.discussion = Discussion.objects.create(
            comment="Hello World, I am a test comment.",
            entry=self.basic_entry,
            author=self.user
        )

        self.reply_discussion = Discussion.objects.create(
            comment="I am a reply",
            entry=self.basic_entry,
            author=self.user,
            parent=self.discussion
        )

    def test_get_delete_view(self):
        """
        Test the the confirm message can be accessed when get
        method is requested from view
        """
        url = reverse('delete_comment', kwargs={
            'module_pk': self.module.module_code,
            'entry_pk': self.basic_entry.pk,
            'pk': self.discussion.pk
        })

        self.run_get_view(url)

    def test_post_delete_view(self):
        url = reverse('delete_comment', kwargs={
            'module_pk': self.module.module_code,
            'entry_pk': self.basic_entry.pk,
            'pk': self.discussion.pk
        })

        response = self.run_valid_post_view(url, {})
        