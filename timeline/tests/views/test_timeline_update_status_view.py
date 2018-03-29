from django.urls import reverse
from timeline.models import TimelineEntry
from .timeline_view_testcase import TimelineViewTestCase


class TimelineUpdateStatusViewTest(TimelineViewTestCase):
    """
    Test case for TimelineUpdateStatus
    """
    pass
    # def setUp(self):
    #     super(TimelineUpdateStatusViewTest, self).setUp()
    #     kwargs = {
    #         'module_pk': self.module.module_code,
    #         'pk': self.entry.pk
    #     }

    #     self.url = reverse('approve_entry', kwargs=kwargs)

    #     kwargs = {
    #         'module_pk': self.module.module_code
    #     }

    #     self.redirect_url = reverse('module_timeline', kwargs=kwargs)

    # def test_get_status_update_request_redirects(self):
    #     """
    #     Test for asserting that a user cannot access the
    #     request if they attempt to use a get request.
    #     """
    #     self.client.force_login(self.admin)
    #     response = self.client.get(self.url)
    #     self.assertEquals(response.status_code, 302)
    #     # check that request was redirected
    #     self.assertEquals(response.url, self.redirect_url)

    # def test_get_status_update_not_logged_in(self):
    #     """
    #     Test to asser that user cannot access view
    #     if not logged in.
    #     """
    #     self.run_get_view_not_logged_in(self.url)
