from django.core.urlresolvers import reverse
from core.tests.common_test_utils import LoggedInTestCase


class UserUpdatePasswordViewTest(LoggedInTestCase):
    """
    Test case for UserUpdatePasswordView, which allows
    users to change thier passwords.
    """
    def setUp(self):
        super(UserUpdatePasswordViewTest, self).setUp()
        session = self.client.session
        # set up the sessions for templates
        session['username'] = self.user.username
        session['user_pk'] = self.user.id
        session.save()

    def test_get_user_update_password_view(self):
        """
        Test case for successfully accesing the password
        as a valid user.
        """
        kwargs = {'slug': self.user.username}
        self.client.force_login(self.user)
        response = self.client.get(reverse('user_password', kwargs=kwargs))
        self.assertEquals(response.status_code, 200)

        # check the form was passed
        context_form = response.context.get("form")()
        password1_field = context_form.__getitem__('password1')
        password2_field = context_form.__getitem__('password2')
        self.assertEquals(password1_field.label, "Password")
        self.assertEquals(password2_field.label, "Confirm Password")

    def test_get_user_update_password_not_logged_in(self):
        """
        Test case for ensuring non logged in user can
        access the form.
        """
        kwargs = {'slug': self.user.username}
        url = reverse('user_password', kwargs=kwargs)
        next_url = reverse('login') + ("?next=" + url)
        response = self.client.get(url)
        self.assertEquals(response.status_code, 302)
        self.assertEquals(response.url, next_url)

    def test_get_user_update_password_for_other_user(self):
        """
        Test case for cehcking that a user cannot access
        another user's password form.
        """
        kwargs = {'slug': "test"}
        self.client.force_login(self.user)
        response = self.client.get(reverse('user_password', kwargs=kwargs))
        self.assertEquals(response.status_code, 302)
        self.assertEquals(response.url, reverse('dashboard'))

    def test_valid_post_user_update_password(self):
        """
        Test case for successfully changing the user's
        password. Then checking user can login with new password.
        """
        kwargs = {'slug': self.user.username}
        next_url = reverse('user_settings', kwargs=kwargs)
        data = {
            'password1': 'new_password',
            'password2': 'new_password'
        }

        self.client.force_login(self.user)
        response = self.client.post(
            reverse('user_password', kwargs=kwargs), data)
        self.assertEquals(response.status_code, 302)
        self.assertEquals(response.url, next_url)

        # logout user to test password was changed
        self.client.logout()

        # login the user with new password
        login = self.client.login(
            username=self.user.username,
            password="new_password"
        )

        # true results in the password being changed
        self.assertTrue(login)

    def test_valid_post_user_update_password_non_matching_passwords(self):
        """
        Test case for checking that non-matching passwords
        will not be accepted by view.
        """
        kwargs = {'slug': self.user.username}
        data = {
            'password1': 'new_password',
            'password2': 'new_pass_word'
        }

        self.client.force_login(self.user)
        response = self.client.post(
            reverse('user_password', kwargs=kwargs), data)

        # since passwords don't match, will redirect to password form
        self.assertEquals(response.status_code, 302)
        self.assertEquals(response.url,
                          reverse('user_password', kwargs=kwargs))

    def test_valid_post_user_update_password_invalid_form(self):
        """
        Test case for checking that view will not accept
        an invlaid form.
        """
        kwargs = {'slug': self.user.username}
        # provide empty dict to trigger invalid form
        data = {}
        self.client.force_login(self.user)
        response = self.client.post(
            reverse('user_password', kwargs=kwargs), data)

        # since invalid form, will redirect to password form
        self.assertEquals(response.status_code, 302)
        self.assertEquals(response.url,
                          reverse('user_password', kwargs=kwargs))

    def test_invalid_post_user_update_password_not_logged_in(self):
        """
        Test case to ensure non-logged in users cannot access view
        """
        kwargs = {'slug': self.user.username}
        url = reverse('user_settings', kwargs=kwargs)
        next_url = reverse('login') + ("?next=" + url)
        data = {
            'password1': 'new_password',
            'password2': 'new_password'
        }

        response = self.client.post(url, data)
        self.assertEquals(response.status_code, 302)
        self.assertEquals(response.url, next_url)

    def test_invalid_post_user_update_password_for_other_user(self):
        """
        Test to ensure that user's cannot post new passwords
        for other users.
        """
        kwargs = {'slug': "tester"}
        data = {
            'password1': 'new_password',
            'password2': 'new_password'
        }

        self.client.force_login(self.user)
        response = self.client.get(
            reverse('user_password', kwargs=kwargs), data)

        self.assertEquals(response.status_code, 302)
        self.assertEquals(response.url, reverse('dashboard'))
