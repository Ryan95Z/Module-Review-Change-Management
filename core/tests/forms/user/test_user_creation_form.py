from django.test import TestCase
from core.forms import UserCreationForm


class UserCreationFormTest(TestCase):
    """
    Unit test for the UserCreationForm class
    """
    def setUp(self):
        self.form = UserCreationForm
        self.std_error = ['This field is required.']

    def test_valid_creation_form(self):
        """
        Test case for providing a valid form
        """
        username = "Tester"
        fname = "user"
        lname = "test"
        email = "test@test.com"

        data = {
            'username': username,
            'first_name': fname,
            'last_name': lname,
            'email': email,
            'is_module_leader': False,
            'is_office_admin': False,
            'is_year_tutor': False,
            'is_module_reviewer': False,
            'is_admin': False
        }

        form = self.form(data)
        # check form is valid
        self.assertTrue(form.is_valid())

        # check the data is valid
        self.assertEquals(form.cleaned_data['username'], username)
        self.assertEquals(form.cleaned_data['first_name'], fname)
        self.assertEquals(form.cleaned_data['last_name'], lname)
        self.assertEquals(form.cleaned_data['email'], email)
        self.assertFalse(form.cleaned_data['is_module_leader'])
        self.assertFalse(form.cleaned_data['is_office_admin'])
        self.assertFalse(form.cleaned_data['is_year_tutor'])
        self.assertFalse(form.cleaned_data['is_module_reviewer'])
        self.assertFalse(form.cleaned_data['is_admin'])

        # check for no errors
        self.assertEquals(form.errors, {})

    def test_invalid_creation_form_empty_data(self):
        """
        Test case when no data is provided to form
        """
        data = {}
        form = self.form(data)

        # these fields produce same error
        fields = ['username', 'first_name', 'last_name', 'email']

        self.assertFalse(form.is_valid())

        for f in fields:
            self.assertEquals(form.errors[f], self.std_error)

        # despite no data, this will evaluate to false
        self.assertFalse(form.cleaned_data['is_module_leader'])
        self.assertFalse(form.cleaned_data['is_office_admin'])
        self.assertFalse(form.cleaned_data['is_year_tutor'])
        self.assertFalse(form.cleaned_data['is_module_reviewer'])
        self.assertFalse(form.cleaned_data['is_admin'])

    def test_invalid_creation_form_some_empty_data(self):
        """
        Test case for when there is some data provided, but
        other parts are missing.
        """
        username = "Tester"
        fname = "user"
        lname = "test"
        data = {
            'username': username,
            'first_name': fname,
            'last_name': lname,
            'is_office_admin': False,
            'is_year_tutor': True,
            'is_module_reviewer': False,
        }

        form = self.form(data)

        self.assertFalse(form.is_valid())

        # check values passed are correct
        self.assertEquals(form.cleaned_data['username'], username)
        self.assertEquals(form.cleaned_data['first_name'], fname)
        self.assertEquals(form.cleaned_data['last_name'], lname)
        self.assertFalse(form.cleaned_data['is_office_admin'])
        self.assertTrue(form.cleaned_data['is_year_tutor'])
        self.assertFalse(form.cleaned_data['is_module_reviewer'])

        # despite not being included, should still be false
        self.assertFalse(form.cleaned_data['is_module_leader'])
        self.assertFalse(form.cleaned_data['is_admin'])

        # see if the missing field gives an error
        self.assertEquals(form.errors['email'], self.std_error)

    def test_save_method_creation_form(self):
        """
        Test case for the .save() method of the UserCreationForm
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

        # save the form, but don't commit
        user = form.save(commit=False)

        # check that the user is correct
        self.assertEquals(user.username, username)
        self.assertEquals(user.first_name, fname)
        self.assertEquals(user.last_name, lname)
        self.assertEquals(user.email, email)
        self.assertFalse(user.is_module_leader)
        self.assertFalse(user.is_office_admin)
        self.assertFalse(user.is_year_tutor)
        self.assertFalse(user.is_module_reviewer)
        self.assertFalse(user.is_admin)
