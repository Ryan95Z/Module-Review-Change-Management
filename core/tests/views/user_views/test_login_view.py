from django.core.urlresolvers import reverse
from core.tests.common_test_utils import LoggedInTestCase


class LoginViewTest(LoggedInTestCase):
    """
    Test case for testing the LoginView
    """
    def setUp(self):
        super(LoginViewTest, self).setUp()

    def test_get_user_login_view(self):
        """
        Test to see we can access the view if not
        logged in.
        """
        response = self.client.get(reverse('login'))
        self.assertEquals(response.status_code, 200)

    def test_get_user_login_view_logged_in_already(self):
        """
        Test to check that if a user is logged in, that they
        are redirected to the dashboard instead of the login.
        """
        self.client.force_login(self.user)
        response = self.client.get(reverse('login'))
        self.assertEquals(response.status_code, 302)
        self.assertEquals(response.url, reverse('dashboard'))

    def test_post_user_login_view_valid_details(self):
        """
        Test to see that we can successfully log into the
        application with correct details.
        """
        data = {'username': 'admin', 'password': 'password'}
        response = self.client.post(reverse('login'), data)
        session = self.client.session
        self.assertEquals(response.status_code, 302)
        self.assertEquals(response.url, reverse('dashboard'))
        self.assertEqual(session["username"], "admin")

    def test_post_user_login_view_invalid_details(self):
        """
        Test to see that if we provide incorrect login detials,
        that we are redirected to the login screen.
        """
        data = {'username': 'admin', 'password': 'badpassword'}
        response = self.client.post(reverse('login'), data)
        self.assertEquals(response.status_code, 302)
        self.assertEquals(response.url, reverse('login'))

    def test_post_user_login_view_blank_details(self):
        """
        Test to see that if we provide blank details
        to the login that we are redirected to login screen.
        """
        data = {'username': '', 'password': ''}
        response = self.client.post(reverse('login'), data)
        self.assertEquals(response.status_code, 302)
        self.assertEquals(response.url, reverse('login'))

    def test_post_user_login_view_logged_in_already(self):
        """
        Test to check that if we are already logged in,
        then we are redirected to the dashboard instead.
        """
        self.client.force_login(self.user)
        data = {'username': 'admin', 'password': 'password'}
        response = self.client.post(reverse('login'), data)
        self.assertEquals(response.status_code, 302)
        self.assertEquals(response.url, reverse('dashboard'))
