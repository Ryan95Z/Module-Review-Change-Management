from django.forms import ValidationError
from django.test import TestCase
from core.forms import UserDetailsForm


class TestUserDetailsForm(TestCase):
    """
    Test case for UserDetailsForm
    """
    def setUp(self):
        super(TestUserDetailsForm, self).setUp()
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
