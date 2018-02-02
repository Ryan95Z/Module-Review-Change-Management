from django.core.urlresolvers import reverse
from core.tests.views.admin_views.admin_test_case import AdminViewTestCase


class TestAdminNewUserView(AdminViewTestCase):
    """
    Test case for AdminNewUserView
    """
    def setUp(self):
        super(TestAdminNewUserView, self).setUp()
        self.url = reverse("new_user")

    def test_get_new_user_view(self):
        """
        Test to get the form if logged in as an admin
        """
        self.run_get_view(self.url)

    def test_get_new_user_incorrect_access(self):
        """
        Test case to check non-admin users cannot access the view
        """
        self.run_get_view_incorrect_access(self.url)

    def test_valid_post_new_user(self):
        """
        Test case for valid post data
        """
        data = {
            'username': 'Test1',
            'first_name': 'John',
            'last_name': 'Tester',
            'email': 'test@test.com'
        }
        response = self.run_valid_post_view(self.url, data)
        self.assertEquals(response.url, reverse('all_users'))

    def test_invalid_post_new_user(self):
        """
        Test case for invalid post data
        """
        data = {
            'username': 'Test1',
            'first_name': 'John',
            'last_name': 'Tester',
            'email': '123'
        }
        self.run_invalid_post_view(self.url, data)
