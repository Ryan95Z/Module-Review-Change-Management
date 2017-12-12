from django.core.urlresolvers import reverse
from core.tests.common_test_utils import LoggedInTestCase


class UserListViewTest(LoggedInTestCase):
    """
    Test case for testing the UserListView
    """

    def setUp(self):
        super(UserListViewTest, self).setUp()
        self.url = reverse('all_users')

    def test_get_user_list_view(self):
        """
        Test to check that if we are logged in as
        a admin, then we can access the view.
        """
        session = self.client.session
        session['username'] = "admin"
        session.save()
        login = self.client.login(username="admin", password="password")
        response = self.client.get(self.url)
        self.assertEquals(response.status_code, 200)

    def test_get_user_list_view_with_incorrect_access(self):
        """
        Test that if we are not a user with the correct
        access rights, then we are redirected to dashboard.
        """
        self.client.force_login(self.user)
        response = self.client.get(self.url)
        self.assertEquals(response.status_code, 302)
        self.assertEquals(response.url, reverse('dashboard'))

    def test_get_user_list_view_not_logged_in(self):
        """
        Test to check that if we are a non-logged in user,
        then we are redirected to the login.
        """
        next_url = reverse('login') + ("?next=" + self.url)
        response = self.client.get(reverse('all_users'))
        self.assertEquals(response.status_code, 302)
        self.assertEquals(response.url, next_url)
