from django.core.urlresolvers import reverse
from core.tests.views.admin_views.admin_test_case import AdminViewTestCase
from core.models import Module


class TestAdminModuleListView(AdminViewTestCase):
    """
    Unit test for AdminModuleListView
    """

    def setUp(self):
        super(TestAdminModuleListView, self).setUp()
        self.url = reverse('all_modules')

    def test_get_module_list_view(self):
        """
        Test case for accessing the view as an admin
        """
        self.run_get_view(self.url)

    def test_get_module_list_view_with_incorrect_access(self):
        """
        Test case to check non-admin users accessing the view
        """
        self.run_get_view_incorrect_access(self.url)

    def test_get_module_list_view_not_logged_in(self):
        """
        Test case to check that non-logged in users cannot access the view
        """
        self.run_get_view_not_logged_in(self.url)
