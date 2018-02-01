from django.core.urlresolvers import reverse
from core.tests.views.admin_views.admin_test_case import AdminViewTestCase
from core.models import User


class TestAdminUpdateUserPermissionsView(AdminViewTestCase):
    def setUp(self):
        super(TestAdminUpdateUserPermissionsView, self).setUp()
        self.kwargs = {'pk': self.admin.id}
        self.url = reverse('edit_user', kwargs=self.kwargs)

    def test_get_update_permission_view(self):
        """
        Test case for accessing the view as an admin
        """
        login = self.client.login(
            username=self.admin.username,
            password=self.admin_password
        )
        response = self.client.get(self.url)
        self.assertEquals(response.status_code, 200)

    def test_get_update_permission_view_with_incorrect_access(self):
        """
        Test case to check that non-admins cannot access the view
        """
        self.client.force_login(self.user)
        response = self.client.get(self.url)
        self.assertEquals(response.status_code, 302)
        self.assertEquals(response.url, reverse('dashboard'))

    def test_get_update_permission_view_not_logged_in(self):
        """
        Test case to prevent non-logged in users from accessing it
        """
        next_url = reverse('login') + ("?next=" + self.url)
        response = self.client.get(self.url)
        self.assertEquals(response.status_code, 302)
        self.assertEquals(response.url, next_url)

    def test_valid_post_update_permissions(self):
        """
        Test case for posting valid data
        """
        data = {
            'is_module_leader': True,
            'is_office_admin': False,
            'is_year_tutor': False,
            'is_admin': True
        }
        # check the permissions before update is applied
        self.assertFalse(self.admin.is_module_leader)
        self.assertTrue(self.admin.is_admin)

        self.client.force_login(self.admin)
        response = self.client.post(self.url, data)
        self.assertEquals(response.status_code, 302)
        self.assertEquals(response.url, reverse('all_users'))

        # check that the changes took place
        admin = User.objects.get(id=self.admin.id)
        self.assertTrue(admin.is_module_leader)
        self.assertTrue(admin.is_admin)
