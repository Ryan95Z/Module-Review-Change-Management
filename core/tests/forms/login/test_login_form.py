from django.test import TestCase
from core.forms import LoginForm


class LoginFormTest(TestCase):
    """
    Test case for login form
    """

    def setUp(self):
        super(LoginFormTest, self).setUp()

    def test_valid_login_form(self):
        """
        Test to check that given valid inforamtion
        the form will work correctly.
        """
        form = LoginForm({
            'username': 'admin',
            'password': 'password'
        })

        # check everything is correct
        self.assertTrue(form.is_valid())
        self.assertEquals(form.cleaned_data['username'], 'admin')
        self.assertEquals(form.cleaned_data['password'], 'password')

    def test_invalid_login_form(self):
        """
        Test to check that form will perform as
        expect when given invalid inforamtion into form
        """
        form = LoginForm({})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['username'], ['This field is required.'])
