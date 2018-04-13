from django.core.urlresolvers import reverse
from timeline.models import Notification
from timeline.tests.views.base_timeline_view_test_case import BaseTimelineViewTestCase


class TestGetNotifications(BaseTimelineViewTestCase):
    """
    Test case for the GetNotifications view
    """
    def setUp(self):
        super(TestGetNotifications, self).setUp()
        self.model = Notification

        self.n1 = self.model.objects.create(
            content="Hello World!",
            recipient=self.admin,
            link="/",
        )

        self.url = reverse('api_notifications')

    def test_get_view(self):
        """
        Test case to ensure that the get method
        is not allowed for this view.
        """
        self.run_get_method_not_allows(self.url)

    def test_post_ajax_with_notifications(self):
        """
        Test case to assert that if there are notifications
        then the flag will give true.
        """
        data = {
            'user': self.admin.username
        }

        response = self.run_valid_ajax(self.url, data)
        self.assertJSONEqual(
            str(response.content, encoding='utf8'),
            {'has_notifications': True}
        )

    def test_post_ajax_with_no_new_notifications(self):
        """
        Test case for assert that if there are no notifications
        then it returns false.
        """
        self.n1.seen = True
        self.n1.save()

        data = {
            'user': self.admin.username
        }

        response = self.run_valid_ajax(self.url, data)
        self.assertJSONEqual(
            str(response.content, encoding='utf8'),
            {'has_notifications': False}
        )
