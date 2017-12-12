from django.forms import ValidationError
from django.test import TestCase
from core.forms import (UserPermissionsForm, UserDetailsForm, UserPasswordForm)
from core.models import User, UserManager


class UserPermissionsFormTest(TestCase):
    """
    Test case for the UserPermissionsForm
    """
    def setUp(self):
        super(UserPermissionsFormTest, self).setUp()
        self.form = UserPermissionsForm

    def test_valid_user_permissions_form(self):
        """
        Test to check that given the correct information
        the form will operate as expected
        """
        data = {
            'is_module_leader': True,
            'is_office_admin': False,
            'is_year_tutor': False,
            'is_admin': False
        }

        form = self.form(data)

        # check that everything is correct
        self.assertTrue(form.is_valid())
        self.assertTrue(form.cleaned_data['is_module_leader'])
        self.assertFalse(form.cleaned_data['is_office_admin'])
        self.assertFalse(form.cleaned_data['is_year_tutor'])
        self.assertFalse(form.cleaned_data['is_admin'])
        self.assertEquals(form.errors, {})

    def test_valid_user_permissions_form_no_data(self):
        """
        Test to check that given a null data, the form
        will default to false for permissions.
        """
        data = {}
        form = self.form(data)

        # since none of the fields are required
        # no data is still valid
        self.assertTrue(form.is_valid())
        self.assertFalse(form.cleaned_data['is_module_leader'])
        self.assertFalse(form.cleaned_data['is_office_admin'])
        self.assertFalse(form.cleaned_data['is_year_tutor'])
        self.assertFalse(form.cleaned_data['is_admin'])
        self.assertEquals(form.errors, {})

    def test_valid_user_permisisons_wrong_data(self):
        """
        Test to check the affects of what happens when
        invalid data is placed into one of the fields.
        """
        data = {
            'is_module_leader': 45656547,
            'is_admin': True
        }

        form = self.form(data)
        # since anything can be cast to a boolean
        # this will always return true despite being invalid
        self.assertTrue(form.is_valid())
        self.assertTrue(form.cleaned_data['is_module_leader'])
        self.assertFalse(form.cleaned_data['is_office_admin'])
        self.assertFalse(form.cleaned_data['is_year_tutor'])
        self.assertTrue(form.cleaned_data['is_admin'])
        self.assertEquals(form.errors, {})


class UserDetailsFormTest(TestCase):
    """
    Test case for UserDetailsForm
    """
    def setUp(self):
        super(UserDetailsFormTest, self).setUp()
        self.form = UserDetailsForm
        self.std_error = ['This field is required.']

    def test_valid_user_details_form(self):
        """
        Test the form with valid data
        """
        username = "Tester"
        fname = "user"
        lname = "test"
        email = "test@test.com"

        data = {
            'username': username,
            'first_name': fname,
            'last_name': lname,
            'email': email
        }

        form = self.form(data)

        self.assertTrue(form.is_valid())
        self.assertEquals(form.cleaned_data['username'], username)
        self.assertEquals(form.cleaned_data['first_name'], fname)
        self.assertEquals(form.cleaned_data['last_name'], lname)
        self.assertEquals(form.cleaned_data['email'], email)
        self.assertEquals(form.errors, {})

    def test_invalid_user_details_form_empty_data(self):
        """
        Test to see form is invalid if given no data
        """
        data = {}
        form = self.form(data)
        fields = ['username', 'first_name', 'last_name', 'email']

        self.assertFalse(form.is_valid())
        # loop through each field as
        # they will all contian the same error
        for f in fields:
            self.assertEquals(form.errors[f], self.std_error)

    def test_invalid_user_details_form_missing_data(self):
        """
        Test case to see that form can still operate
        even if some required data is missing. If the data is
        missing, then we do get the correct error.
        """
        username = "Tester"
        fname = "user"
        lname = "test"
        data = {
            'username': username,
            'first_name': fname,
            'last_name': lname
        }
        form = self.form(data)

        self.assertFalse(form.is_valid())
        # despite form being invalid, we can access the valid data
        self.assertEquals(form.cleaned_data['username'], username)
        self.assertEquals(form.cleaned_data['first_name'], fname)
        self.assertEquals(form.cleaned_data['last_name'], lname)
        # see if the error we expect is there
        self.assertEquals(form.errors['email'], self.std_error)


class UserPasswordFormTest(TestCase):
    """
    Test case for UserPasswordForm
    """
    def setUp(self):
        super(UserPasswordFormTest, self).setUp()
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
