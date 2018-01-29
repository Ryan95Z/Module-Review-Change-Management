from django.core.urlresolvers import reverse
from core.tests.common_test_utils import LoggedInTestCase


class UserSettingsViewTest(LoggedInTestCase):
    """
    Test case for UserSettingsView
    """
    def setUp(self):
        super(UserSettingsViewTest, self).setUp()
        session = self.client.session
        # set up the sessions for templates
        session['username'] = self.user.username
        session['user_pk'] = self.user.id
        session.save()

    def test_get_user_settings_view(self):
        """
        Test for getting the view as a valid user
        """
        kwargs = {'slug': "user1"}
        self.client.force_login(self.user)
        response = self.client.get(reverse('user_settings', kwargs=kwargs))
        self.assertEquals(response.status_code, 200)

    def test_get_user_settings_not_logged_in(self):
        """
        Test case for check the user is redirected to the
        login if they are not logged in.
        """
        kwargs = {'slug': "user1"}
        next_url = ("?next=") + reverse('user_settings', kwargs=kwargs)
        response = self.client.get(reverse('user_settings', kwargs=kwargs))
        self.assertEquals(response.status_code, 302)
        self.assertEqual(response.url, (reverse('login') + next_url))

    def test_get_user_settings_for_other_users(self):
        """
        Test case to check that a user is redirected
        if they try to access another user's inforamtion
        """
        kwargs = {'slug': "admin"}
        self.client.force_login(self.user)
        response = self.client.get(reverse('user_settings', kwargs=kwargs))
        self.assertEquals(response.status_code, 302)
        self.assertEquals(response.url, reverse('dashboard'))
