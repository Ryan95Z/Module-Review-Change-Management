from django.test import TestCase
from core.forms import SearchForm


class TestSearchForm(TestCase):
    """
    Unit test for SearchForm
    """
    def setUp(self):
        super(TestSearchForm, self).setUp()
        self.form = SearchForm

    def test_valid_search_form(self):
        """
        Test case for string input
        """
        SEARCH = 'hello world'

        form = self.form({
            'search': SEARCH
        })

        self.assertTrue(form.is_valid())
        self.assertEquals(form.cleaned_data['search'], SEARCH)

    def test_search_with_integer(self):
        """
        Test case to ensure form can handle other types, such
        as an integer
        """
        SEARCH = 4000
        form = self.form({
            'search': SEARCH
        })

        self.assertTrue(form.is_valid())
        # check that int value is converted to string
        self.assertEquals(form.cleaned_data['search'], str(SEARCH))

    def test_search_with_blank_data(self):
        err = ['This field is required.']
        form = self.form({
            'search': ''
        })

        # invalid form as it has empty value
        self.assertFalse(form.is_valid())

        # check that an error was provided
        self.assertEquals(form.errors['search'], err)

    def test_search_with_none_value(self):
        """
        Test case for checking that the form
        is invalid if provided with None.
        """
        err = ['This field is required.']
        form = self.form({
            'search': None
        })

        self.assertFalse(form.is_valid())
        self.assertEquals(form.errors['search'], err)
