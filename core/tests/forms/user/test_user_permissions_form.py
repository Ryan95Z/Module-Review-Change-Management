from django.test import TestCase
from core.forms import UserPermissionsForm


class TestUserPermissionsForm(TestCase):
    """
    Unit test for the UserPermissionsForm
    """
    def setUp(self):
        super(TestUserPermissionsForm, self).setUp()
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
            'is_module_reviewer': True,
            'is_admin': False
        }

        form = self.form(data)

        # check that everything is correct
        self.assertTrue(form.is_valid())
        self.assertTrue(form.cleaned_data['is_module_leader'])
        self.assertFalse(form.cleaned_data['is_office_admin'])
        self.assertFalse(form.cleaned_data['is_year_tutor'])
        self.assertTrue(form.cleaned_data['is_module_reviewer'])
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
        self.assertFalse(form.cleaned_data['is_module_reviewer'])
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
        self.assertFalse(form.cleaned_data['is_module_reviewer'])
        self.assertTrue(form.cleaned_data['is_admin'])
        self.assertEquals(form.errors, {})
