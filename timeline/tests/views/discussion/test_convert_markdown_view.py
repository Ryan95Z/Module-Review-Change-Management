from django.core.urlresolvers import reverse
from timeline.tests.views.base_timeline_view_test_case import BaseTimelineViewTestCase


class TestConvertMarkdownView(BaseTimelineViewTestCase):
    """
    Test case for ConvertMarkdownView view
    """
    def setUp(self):
        super(TestConvertMarkdownView, self).setUp()
        self.url = reverse('api_markdown')

    def test_method_not_allowed_get(self):
        """
        Test get method cannot be accessed
        """
        self.run_get_method_not_allows(self.url)

    def test_post_now_allowed_without_ajax(self):
        """
        Test post with ajax cannot be accessed
        """
        data = {'markdown': 'I am some data'}
        self.run_post_not_allowed(self.url, data)

    def test_post_with_ajax(self):
        """
        Test markdown is converted when ajax request is used.
        """
        data = {'markdown': '* Hello\n * World\n'}
        response = self.run_valid_ajax(self.url, data)
        expected_result = {
            "markdown": "<ul>\n<li>Hello </li>\n<li>World </li>\n</ul>"
        }
        self.assertJSONEqual(
            str(response.content, encoding='utf8'),
            expected_result
        )
