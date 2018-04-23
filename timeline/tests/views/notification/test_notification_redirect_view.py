from django.core.urlresolvers import reverse
from timeline.models import Notification
from timeline.tests.views.base_timeline_view_test_case import BaseTimelineViewTestCase


class TestNotificationRedirectView(BaseTimelineViewTestCase):
    """
    Test case for the NotificationRedirect View
    """
    def setUp(self):
        super(TestNotificationRedirectView, self).setUp()
        self.model = Notification

        self.n1 = self.model.objects.create(
            content="Goodbye World!",
            recipient=self.admin,
            link="/"
        )

        self.url = reverse('notification_redirect', kwargs={
            'pk': self.n1.pk
        })

    def test_valid_redirect_of_notification(self):
        """
        Test that notification will redirect and will
        update if it has been seen.
        """
        self.client.login(
            username=self.admin.username,
            password=self.admin_password
        )

        # check the notification has not been seen
        pre_seen_notice = self.model.objects.get(id=self.n1.pk)
        self.assertFalse(pre_seen_notice.seen)

        response = self.client.get(self.url)
        self.assertEquals(response.status_code, 302)
        self.assertEquals(response.url, self.n1.link)

        # check that the notification has now been seen
        post_seen_notice = self.model.objects.get(id=self.n1.pk)
        self.assertTrue(post_seen_notice.seen)

    def test_invalid_id_for_notification(self):
        """
        Test to assert that a 404 is raised if an invlaid
        id for the notification model is provided.
        """
        self.client.login(
            username=self.admin.username,
            password=self.admin_password
        )

        url = reverse('notification_redirect', kwargs={
            'pk': 20035
        })

        # assert that 404 is raised if invalid model id
        response = self.client.get(url)
        self.assertEquals(response.status_code, 404)
