from django.core.urlresolvers import reverse
from core.tests.common_test_utils import LoggedInTestCase


class LogoutViewTest(LoggedInTestCase):
    """
    Test case for testing the Logout view
    """

    def test_get_user_logout_view(self):
        """
        Test to see that we are redirect correctly,
        when we log out as a user.
        """

        # configure the session
        session = self.client.session
        session['user_pk'] = self.user.id
        session['username'] = self.user.username
        session.save()
        self.client.force_login(self.user)
        response = self.client.get(reverse('logout'))
        self.assertEquals(response.status_code, 302)
        self.assertEquals(response.url, reverse('login'))

    def test_get_user_logout_view_not_logged_in(self):
        """
        Test to check that even if we are not logged in,
        that we are still redirect to the login.
        """
        response = self.client.get(reverse('logout'))
        self.assertEquals(response.status_code, 302)
        self.assertEquals(response.url, reverse('login'))
