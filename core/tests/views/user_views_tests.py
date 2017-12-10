from django.core.urlresolvers import reverse_lazy
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
        response = self.client.get(reverse_lazy('login'))
        self.assertEquals(response.status_code, 200)

    def test_get_user_login_view_logged_in_already(self):
        """
        Test to check that if a user is logged in, that they
        are redirected to the dashboard instead of the login.
        """
        self.client.force_login(self.user)
        response = self.client.get(reverse_lazy('login'))
        self.assertEquals(response.status_code, 302)
        self.assertEquals(response.url, reverse_lazy('dashboard'))

    def test_post_user_login_view_valid_details(self):
        """
        Test to see that we can successfully log into the
        application with correct details.
        """
        data = {'username': 'admin', 'password': 'password'}
        response = self.client.post(reverse_lazy('login'), data)
        session = self.client.session
        self.assertEquals(response.status_code, 302)
        self.assertEquals(response.url, reverse_lazy('dashboard'))
        self.assertEqual(session["username"], "admin")

    def test_post_user_login_view_invalid_details(self):
        """
        Test to see that if we provide incorrect login detials,
        that we are redirected to the login screen.
        """
        data = {'username': 'admin', 'password': 'badpassword'}
        response = self.client.post(reverse_lazy('login'), data)
        self.assertEquals(response.status_code, 302)
        self.assertEquals(response.url, reverse_lazy('login'))

    def test_post_user_login_view_blank_details(self):
        """
        Test to see that if we provide blank details
        to the login that we are redirected to login screen.
        """
        data = {'username': '', 'password': ''}
        response = self.client.post(reverse_lazy('login'), data)
        self.assertEquals(response.status_code, 302)
        self.assertEquals(response.url, reverse_lazy('login'))

    def test_post_user_login_view_logged_in_already(self):
        """
        Test to check that if we are already logged in,
        then we are redirected to the dashboard instead.
        """
        self.client.force_login(self.user)
        data = {'username': 'admin', 'password': 'password'}
        response = self.client.post(reverse_lazy('login'), data)
        self.assertEquals(response.status_code, 302)
        self.assertEquals(response.url, reverse_lazy('dashboard'))


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
        response = self.client.get(reverse_lazy('logout'))
        self.assertEquals(response.status_code, 302)
        self.assertEquals(response.url, reverse_lazy('login'))

    def test_get_user_logout_view_not_logged_in(self):
        """
        Test to check that even if we are not logged in,
        that we are still redirect to the login.
        """
        response = self.client.get(reverse_lazy('logout'))
        self.assertEquals(response.status_code, 302)
        self.assertEquals(response.url, reverse_lazy('login'))


class UserListViewTest(LoggedInTestCase):
    """
    Test case for testing the UserListView
    """

    def setUp(self):
        super(UserListViewTest, self).setUp()

    def test_get_user_list_view(self):
        """
        Test to check that if we are logged in as
        a admin, then we can access the view.
        """
        session = self.client.session
        session['username'] = "admin"
        session.save()
        login = self.client.login(username="admin", password="password")
        response = self.client.get(reverse_lazy('all_users'))
        self.assertEquals(response.status_code, 200)

    def test_get_user_list_view_with_incorrect_access(self):
        """
        Test that if we are not a user with the correct
        access rights, then we are redirected to dashboard.
        """
        self.client.force_login(self.user)
        response = self.client.get(reverse_lazy('all_users'))
        self.assertEquals(response.status_code, 302)
        self.assertEquals(response.url, reverse_lazy('dashboard'))

    def test_get_user_list_view_not_logged_in(self):
        """
        Test to check that if we are a non-logged in user,
        then we are redirected to the login.
        """
        response = self.client.get(reverse_lazy('all_users'))
        self.assertEquals(response.status_code, 302)
        self.assertEquals(response.url, reverse_lazy('login'))
