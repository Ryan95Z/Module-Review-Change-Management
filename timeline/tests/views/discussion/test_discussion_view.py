from json import loads
from django.core.urlresolvers import reverse
from timeline.models import TimelineEntry, Discussion
from timeline.tests.views.base_timeline_view_test_case import BaseTimelineViewTestCase


class TestDiscussionView(BaseTimelineViewTestCase):
    """
    Test case for the DiscussionView class
    """
    def setUp(self):
        super(TestDiscussionView, self).setUp()
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

        self.discussion_one = Discussion.objects.create(
            comment="Hello World, I am a test comment.",
            entry=self.basic_entry,
            author=self.user
        )

        self.discussion_two = Discussion.objects.create(
            comment="Hello World, I am a new comment.",
            entry=self.basic_entry,
            author=self.user
        )

        self.url = reverse('discussion', kwargs={
            'module_pk': self.module.module_code,
            'pk': self.basic_entry.pk,
        })

    def test_get_discussion_view(self):
        """
        Test to get the discussion view
        """
        response = self.run_get_view(self.url)
        context = response.context
        self.assertEquals(context['entry_id'], str(self.basic_entry.pk))
        self.assertEquals(context['module_code'], self.module.module_code)
        self.assertEquals(context['entry'], self.basic_entry)

    def test_post_new_discussion(self):
        """
        Test to assert that new comments are added when post request used.
        """
        data = {
            'comment': "Hello World, I am a new comment"
        }

        # check that the new comment does not exist
        discussion = Discussion.objects.filter(entry=self.basic_entry)
        self.assertEquals(discussion.count(), 2)

        response = self.run_valid_post_view(self.url, data)
        self.assertEquals(response.url, self.url)

        # check that the comment has been added.
        discussion = Discussion.objects.filter(entry=self.basic_entry)
        self.assertEquals(discussion.count(), 3)

    def test_post_new_reply(self):
        """
        Test that comment replies are added when a post request is made.
        """
        data = {
            'comment': "I am a reply",
            'parent': self.discussion_one.pk
        }

        # check that the new comment does not exist
        discussion = Discussion.objects.filter(entry=self.basic_entry)
        self.assertEquals(discussion.count(), 2)

        response = self.run_valid_post_view(self.url, data)
        self.assertEquals(response.url, self.url)

        # check that the comment has been added.
        discussion = Discussion.objects.filter(entry=self.basic_entry)
        self.assertEquals(discussion.count(), 3)

    def test_post_new_discussion_ajax(self):
        """
        Test the creation of a comment via  ajax post request
        """
        data = {
            'comment': "Hello World, I am a new comment"
        }

        # kwargs for delete and edit urls
        kwargs = {
            'module_pk': self.module.module_code,
            'entry_pk': self.basic_entry.pk,
            'pk': self.discussion_two.pk + 1
        }

        # kwargs for authors profile
        author_kwargs = {'pk': self.admin.pk}

        # urls
        edit_url = reverse('edit_comment', kwargs=kwargs)
        delete_url = reverse('delete_comment', kwargs=kwargs)
        profile_url = reverse('user_profile', kwargs=author_kwargs)

        # check that the new comment does not exist
        discussion = Discussion.objects.filter(entry=self.basic_entry)
        self.assertEquals(discussion.count(), 2)

        # get the json and check it
        response = self.run_valid_ajax(self.url, data)
        json = loads(str(response.content, encoding='utf8'))

        expected_content = "<p>{}</p>".format(data['comment'])

        self.assertEquals(json['md'], data['comment'])
        self.assertEquals(json['content'], expected_content)
        self.assertEquals(json['author'], self.admin.username)
        self.assertEquals(json['time'], "just now")

        self.assertEquals(json['edit_url'], edit_url)
        self.assertEquals(json['delete_url'], delete_url)
        self.assertEquals(json['author_url'], profile_url)
