from django.core.urlresolvers import reverse
from core.tests.views.admin_views.admin_test_case import AdminViewTestCase
from core.models import Module


class TestAdminModuleListView(AdminViewTestCase):

    def setUp(self):
        super(TestAdminModuleListView, self).setUp()
        self.url = reverse('all_modules')

    def test_get_module_list_view(self):
        """
        Test case for accessing the view as an admin
        """
        login = self.client.login(
            username=self.admin.username,
            password=self.admin_password
        )
        response = self.client.get(self.url)
        self.assertEquals(response.status_code, 200)

    def test_get_module_list_view_with_incorrect_access(self):
        """
        Test case to check non-admin users accessing the view
        """
        self.client.force_login(self.user)
        response = self.client.get(self.url)
        self.assertEquals(response.status_code, 302)
        self.assertEquals(response.url, reverse('dashboard'))

    def test_get_module_list_view_not_logged_in(self):
        """
        Test case to check that non-logged in users cannot access the view
        """
        next_url = reverse('login') + ("?next=" + self.url)
        response = self.client.get(self.url)
        self.assertEquals(response.status_code, 302)
        self.assertEquals(response.url, next_url)
