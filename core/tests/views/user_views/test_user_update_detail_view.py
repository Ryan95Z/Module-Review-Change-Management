from django.core.urlresolvers import reverse
from core.tests.common_test_utils import LoggedInTestCase
from core.models import User


class UserUpdateDetailsViewTest(LoggedInTestCase):
    """
    Test case for the UserUpdateDetailsView
    """
    def setUp(self):
        super(UserUpdateDetailsViewTest, self).setUp()
        session = self.client.session
        # set up the sessions for templates
        session['username'] = self.user.username
        session['user_pk'] = self.user.id
        session.save()

    def test_get_user_update_details(self):
        """
        Test for accessing the view as a standard user
        with correct access rights.
        """
        kwargs = {'slug': "user1"}
        self.client.force_login(self.user)
        response = self.client.get(reverse('user_details', kwargs=kwargs))
        self.assertEquals(response.status_code, 200)

    def test_get_user_update_not_logged_in(self):
        """
        Test to check that the user is directed to the
        login screen if they are not loged in.
        """
        kwargs = {'slug': "user1"}
        next_url = ("?next=") + reverse('user_details', kwargs=kwargs)
        response = self.client.get(reverse('user_details', kwargs=kwargs))
        self.assertEquals(response.status_code, 302)
        self.assertEqual(response.url, reverse('login') + next_url)

    def test_get_user_update_details_for_other_user(self):
        """
        Test to ensure that user cannot access details
        of another user and are redirected.
        """
        kwargs = {'slug': "admin"}
        self.client.force_login(self.user)
        response = self.client.get(reverse('user_details', kwargs=kwargs))
        self.assertEquals(response.status_code, 302)
        self.assertEquals(response.url, reverse('dashboard'))

    def test_valid_post_user_details(self):
        """
        Test view with valid post information
        by changing the first_name of the user.
        """
        data = {
            'username': self.user.username,
            'first_name': "tester",
            'last_name': self.user.last_name,
            'email': self.user.email
        }

        kwargs = {'slug': self.user.username}
        self.client.force_login(self.user)
        response = self.client.post(
            reverse('user_details', kwargs=kwargs), data)
        self.assertEquals(response.status_code, 302)
        self.assertEquals(response.url,
                          reverse('user_settings', kwargs=kwargs))

        # check that the user was updated
        user = User.objects.get(id=self.user.id)
        self.assertEquals(user.first_name, "tester")

    def test_invalid_post_user_details_not_logged_in(self):
        """
        Test form cannot be updated if the user is
        not logged in.
        """
        data = {
            'username': self.user.username,
            'first_name': "tester",
            'last_name': self.user.last_name,
            'email': self.user.email
        }
        kwargs = {'slug': self.user.username}
        next_url = ("?next=") + reverse('user_details', kwargs=kwargs)
        response = self.client.post(
            reverse('user_details', kwargs=kwargs), data)
        self.assertEquals(response.status_code, 302)
        self.assertEqual(response.url, reverse('login') + next_url)

        # check the user's inforamtion Was not change
        user = User.objects.get(id=self.user.id)
        self.assertEquals(user.first_name, "user")
        self.assertNotEquals(user.first_name, "tester")

    def test_invalid_post_user_details_for_other_user(self):
        """
        Test that a user cannot post inforamtion regarding
        another user and change thier inforamtion
        """
        data = {
            'username': self.user.username,
            'first_name': "tester",
            'last_name': self.user.last_name,
            'email': self.user.email
        }

        kwargs = {'slug': "test"}
        self.client.force_login(self.user)
        response = self.client.post(
            reverse('user_details', kwargs=kwargs), data)
        self.assertEquals(response.status_code, 302)
        self.assertEquals(response.url, reverse('dashboard'))

        # check the user's inforamtion Was not change
        user = User.objects.get(id=self.user.id)
        self.assertEquals(user.first_name, "user")
        self.assertNotEquals(user.first_name, "tester")
