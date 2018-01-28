from django.core.urlresolvers import reverse
from core.tests.common_test_utils import LoggedInTestCase
from core.models import User


class TestAdminYearTutorListView(LoggedInTestCase):

    def setUp(self):
        super(TestAdminYearTutorListView, self).setUp()
        self.url = reverse('all_year_tutors')
        session = self.client.session
        session['username'] = "admin"
        session.save()

    def test_get_tutor_list_view(self):
        """
        Test case for accessing the view as an admin
        """
        login = self.client.login(username="admin", password="password")
        response = self.client.get(self.url)
        self.assertEquals(response.status_code, 200)

    def test_get_tutor_list_view_with_incorrect_access(self):
        """
        Test case to check non-admin users accessing the view
        """
        self.client.force_login(self.user)
        response = self.client.get(self.url)
        self.assertEquals(response.status_code, 302)
        self.assertEquals(response.url, reverse('dashboard'))

    def test_get_tutor_list_view_not_logged_in(self):
        """
        Test case to check that non-logged in users cannot access the view
        """
        next_url = reverse('login') + ("?next=" + self.url)
        response = self.client.get(self.url)
        self.assertEquals(response.status_code, 302)
        self.assertEquals(response.url, next_url)
