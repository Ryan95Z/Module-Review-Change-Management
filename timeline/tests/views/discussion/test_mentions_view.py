from django.core.urlresolvers import reverse
from timeline.tests.views.base_timeline_view_test_case import BaseTimelineViewTestCase


class TestMentionsView(BaseTimelineViewTestCase):
    """
    Test case for discussions MentionsView
    """
    def setUp(self):
        super(TestMentionsView, self).setUp()
        self.url = reverse('api_mentions')

    def test_get_mentions_view(self):
        """
        Test that the view is not allowed to have a
        get request made to it.
        """
        self.run_get_method_not_allows(self.url)

    def test_post_mentions_view(self):
        """
        Test post method with valid search term
        """
        data = {
            'mentions': "u"
        }

        response = self.run_valid_post_view_no_redirect(self.url, data)
        self.assertJSONEqual(
            str(response.content, encoding='utf8'),
            {"usernames": [{"username": "user1"}]}
        )

    def test_post_mentions_view_no_results(self):
        """
        Test mentions post request with no valid usernames found
        """
        data = {
            'mentions': "Ryan"
        }

        response = self.run_valid_post_view_no_redirect(self.url, data)
        self.assertJSONEqual(
            str(response.content, encoding='utf8'),
            {"usernames": []}
        )

    def test_ajax_post_of_mentions(self):
        """
        Test the mentions view as a ajax request
        """
        data = {
            'mentions': "u"
        }

        response = self.run_valid_ajax(self.url, data)
        self.assertJSONEqual(
            str(response.content, encoding='utf8'),
            {"usernames": [{"username": "user1"}]}
        )
