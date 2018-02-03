from django.core.urlresolvers import reverse
from core.tests.views.admin_views.admin_test_case import AdminViewTestCase
from core.models import User


class AdminUserListViewTest(AdminViewTestCase):
    """
    Test case for testing the UserListView
    """

    def setUp(self):
        super(AdminUserListViewTest, self).setUp()
        self.url = reverse('all_users')

    def test_get_user_list_view(self):
        """
        Test to check that if we are logged in as
        a admin, then we can access the view.
        """
        self.run_get_view(self.url)

    def test_get_user_list_view_with_incorrect_access(self):
        """
        Test that if we are not a user with the correct
        access rights, then we are redirected to dashboard.
        """
        self.run_get_view_incorrect_access(self.url)

    def test_get_user_list_view_not_logged_in(self):
        """
        Test to check that if we are a non-logged in user,
        then we are redirected to the login.
        """
        self.run_get_view_not_logged_in(self.url)
