from django.forms import ValidationError
from django.test import TestCase
from core.forms import UserPasswordForm
from core.models import User, UserManager


class TestUserPasswordForm(TestCase):
    """
    Unit for UserPasswordForm
    """
    def setUp(self):
        super(TestUserPasswordForm, self).setUp()
        # test user to check that the password is changed
        self.manager = UserManager()
        self.manager.model = User
        self.user = self.manager.create_user(
            username="Test",
            first_name="test",
            last_name="tester",
            email="test@test.com",
            password="password"
        )
        self.form = UserPasswordForm
        self.std_error = ['This field is required.']

    def test_valid_password_form(self):
        password1 = "new_password"
        password2 = "new_password"

        data = {
            'password1': password1,
            'password2': password2
        }

        form = self.form(data)

        # check that the form is valid
        self.assertTrue(form.is_valid())
        self.assertEquals(form.cleaned_data['password1'], password1)
        self.assertEquals(form.cleaned_data['password2'], password2)
        self.assertEquals(form.errors, {})

        # check that the passwords match
        self.assertEquals(form.clean_password(), password1)

        # check that the password is updated for a user
        self.assertTrue(form.update_password(self.user.id))

    def test_valid_password_form_mismatch_data(self):
        """
        Test case for checking how the form handles
        password mismatch.
        """
        password1 = "new_password1"
        password2 = "new_password2"

        data = {
            'password1': password1,
            'password2': password2
        }

        form = self.form(data)

        # check that the form is valid
        self.assertTrue(form.is_valid())
        self.assertEquals(form.cleaned_data['password1'], password1)
        self.assertEquals(form.cleaned_data['password2'], password2)
        self.assertEquals(form.errors, {})

        # check exception is raise when cleaning password
        with self.assertRaises(ValidationError):
            form.clean_password()

        # check password cannot be processed
        self.assertFalse(form.update_password(self.user.id))

    def test_invalid_password_form_empty_data(self):
        """
        Test case to see how form handles empty data
        """
        data = {}
        form = self.form(data)

        self.assertFalse(form.is_valid())
        self.assertEquals(form.errors['password1'], self.std_error)
        self.assertEquals(form.errors['password2'], self.std_error)

        # check that empty data raises an exception
        with self.assertRaises(ValidationError):
            form.clean_password()

        # cannot update the password so returns false
        self.assertFalse(form.update_password(self.user.id))

    def test_update_password_method_with_invlaid_params(self):
        """
        Test case for possible cases that could occur for with
        an invalid user_id parameter.
        """
        # provide valid input to test the method
        password1 = "new_password1"
        password2 = "new_password2"

        data = {
            'password1': password1,
            'password2': password2
        }

        form = self.form(data)

        # test the method with negative numbers
        self.assertFalse(form.update_password(-13))
        self.assertFalse(form.update_password(-1358584))

        # test with zero
        self.assertFalse(form.update_password(0))

        # test with an invalid user id
        self.assertFalse(form.update_password(1000))
        self.assertFalse(form.update_password(100045456))
