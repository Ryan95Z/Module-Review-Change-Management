from django.core.urlresolvers import reverse
from core.tests.common_test_utils import LoggedInTestCase


class DashboardViewTest(LoggedInTestCase):
    """
    Test case for the DashboardView / application index
    """
    def setUp(self):
        super(DashboardViewTest, self).setUp()
        self.url = reverse('dashboard')

    def test_get_dashboard_view(self):
        """
        Test case for accessing the view when logged in
        """
        session = self.client.session
        session['username'] = self.user.username
        session.save()

        login = self.client.force_login(self.user)
        response = self.client.get(self.url)
        self.assertEquals(response.status_code, 200)

    def test_get_dashboard_not_logged_in(self):
        """
        Test case for attempting to access the dashboard
        when not logged in.
        """
        next_url = reverse('login') + ("?next=" + self.url)
        response = self.client.get(self.url)
        self.assertEquals(response.status_code, 302)
        self.assertEquals(response.url, next_url)
