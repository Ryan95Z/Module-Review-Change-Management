from django.core.urlresolvers import reverse
from timeline.models import TimelineEntry, Discussion
from timeline.tests.views.base_timeline_view_test_case import BaseTimelineViewTestCase


class TestDiscussionUpdateView(BaseTimelineViewTestCase):
    """
    Test case for DiscussionUpdateView
    """
    def setUp(self):
        super(TestDiscussionUpdateView, self).setUp()
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

        self.base_comment = "Hello World, I am a test comment."
        self.discussion = Discussion.objects.create(
            comment=self.base_comment,
            entry=self.basic_entry,
            author=self.user
        )

        self.url = reverse('edit_comment', kwargs={
            'module_pk': self.module.module_code,
            'entry_pk': self.basic_entry.pk,
            'pk': self.discussion.pk
        })

    def test_get_update_view(self):
        """
        Test case to get the view
        """
        self.run_get_view(self.url)

    def test_post_update_comment(self):
        """
        Test case for updating a comment with a standard post request
        """
        data = {
            'comment': "I have been updated. Whoop!"
        }

        redirect = reverse('discussion', kwargs={
            'module_pk': self.module.module_code,
            'pk': self.basic_entry.pk
        })

        # check the discussion before update
        discussion = Discussion.objects.get(id=self.discussion.pk)
        self.assertEqual(discussion.comment, self.base_comment)

        # make the update
        response = self.run_valid_post_view(self.url, data)
        self.assertEqual(response.url, redirect)

        # check discussion after update
        discussion = Discussion.objects.get(id=self.discussion.pk)
        self.assertEqual(discussion.comment, data['comment'])

    def test_post_update_comment_ajax(self):
        """
        Test case for updating a comment with ajax post request
        """
        data = {
            'comment': "I have been updated by AJAX. Whoop!"
        }

        expected_json = {
            "html": "<p>{}</p>".format(data['comment']),
            "md": data['comment']
        }

        # check the discussion before update
        discussion = Discussion.objects.get(id=self.discussion.pk)
        self.assertEqual(discussion.comment, self.base_comment)

        # make the update
        response = self.run_valid_ajax(self.url, data)

        # check the json
        self.assertJSONEqual(
            str(response.content, encoding='utf8'),
            expected_json
        )

        # check discussion after update
        discussion = Discussion.objects.get(id=self.discussion.pk)
        self.assertEqual(discussion.comment, data['comment'])