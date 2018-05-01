from django.core.urlresolvers import reverse
from timeline.models import Notification
from timeline.tests.views.base_timeline_view_test_case import BaseTimelineViewTestCase


class TestNotificationHubView(BaseTimelineViewTestCase):
    """
    Test case for the NotificationHub View
    """
    def setUp(self):
        super(TestNotificationHubView, self).setUp()
        self.model = Notification

        self.n1 = self.model.objects.create(
            content="Hello World!",
            recipient=self.admin,
            link="/",
            seen=True
        )

        self.n2 = self.model.objects.create(
            content="Goodbye World!",
            recipient=self.admin,
            link="/"
        )

        self.n3 = self.model.objects.create(
            content="No place like 127.0.0.1!",
            recipient=self.admin,
            link="/"
        )

        self.url = reverse('all_notification')

    def test_get_notification_hub(self):
        """
        Test to get the view
        """
        # get the view
        context = self.run_get_view(self.url).context

        # check the data that is produced
        self.assertEquals(context['unseen'].count(), 2)
        self.assertEquals(context['all'].count(), 3)
        self.assertEquals(context['watching'].count(), 0)
