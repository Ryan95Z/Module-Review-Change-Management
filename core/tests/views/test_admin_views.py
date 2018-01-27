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
        response = self.client.get(self.url)
        self.assertEquals(response.status_code, 302)
        self.assertEquals(response.url, next_url)


class TestAdminNewUserView(LoggedInTestCase):
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
        session = self.client.session
        session['username'] = "admin"
        session.save()
        self.client.login(username="admin", password="password")
        response = self.client.get(self.url)
        self.assertEquals(response.status_code, 200)

    def test_get_new_user_incorrect_access(self):
        """
        Test case to check non-admin users cannot access the view
        """
        self.client.force_login(self.user)
        response = self.client.get(self.url)
        self.assertEquals(response.status_code, 302)
        self.assertEquals(response.url, reverse('dashboard'))

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
        self.client.force_login(self.admin)
        response = self.client.post(reverse('new_user'), data)
        self.assertEquals(response.status_code, 302)
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
        # session required to allow template to render correctly
        session = self.client.session
        session['username'] = "admin"
        session.save()
        self.client.login(username="admin", password="password")
        response = self.client.post(self.url, data)
        self.assertEquals(response.status_code, 200)


class TestAdminYearTutorListView(LoggedInTestCase):

    def setUp(self):
        super(TestAdminYearTutorListView, self).setUp()
        self.url = reverse('all_year_tutors')

    def test_get_tutor_list_view(self):
        """
        """
        session = self.client.session
        session['username'] = "admin"
        session.save()
        login = self.client.login(username="admin", password="password")
        response = self.client.get(self.url)
        self.assertEquals(response.status_code, 200)

    def test_get_tutor_list_view_with_incorrect_access(self):
        """
        """
        self.client.force_login(self.user)
        response = self.client.get(self.url)
        self.assertEquals(response.status_code, 302)
        self.assertEquals(response.url, reverse('dashboard'))

    def test_get_tutor_list_view_not_logged_in(self):
        """
        """
        next_url = reverse('login') + ("?next=" + self.url)
        response = self.client.get(self.url)
        self.assertEquals(response.status_code, 302)
        self.assertEquals(response.url, next_url)
