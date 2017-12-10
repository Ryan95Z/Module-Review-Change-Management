from django.core.urlresolvers import reverse_lazy
from core.tests.common_test_utils import LoggedInTestCase


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
        self.assertEquals(response.url,
                          reverse_lazy('login') + "?next=/users/all/")
