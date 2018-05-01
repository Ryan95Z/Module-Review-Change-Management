from django.core.urlresolvers import reverse
from core.tests.views.admin_views.admin_test_case import AdminViewTestCase
from core.models import Module, ModuleManager


class TestAdminModuleUpdateView(AdminViewTestCase):
    """
    Unit test for testing the AdminModuleUpdateView
    """
    def setUp(self):
        super(TestAdminModuleUpdateView, self).setUp()
        manager = ModuleManager()
        manager.model = Module
        self.module = manager.create_module(
                'CM3301',
                'Software Engineering Project',
                40,
                'L6',
                'Autumn Semester',
                'English',
                self.user
        )
        kwargs = {'pk': self.module.module_code}
        self.url = reverse('update_module', kwargs=kwargs)

    def test_get_module_update_view(self):
        """
        Test case for accessing the view
        """
        response = self.run_get_view(self.url)
        context = response.context

        self.assertEquals(context['form_url'], self.url)
        self.assertEquals(context['form_type'], 'Update')

    def get_module_update_view_incorrect_access(self):
        """
        Test case for checking non-admin users can access view
        """
        self.run_get_view_incorrect_access(self.url)

    def get_module_update_view_not_logged_in(self):
        """
        Test case for non-logged in user
        """
        self.run_get_view_not_logged_in(self.url)

    def test_valid_post_update_view(self):
        """
        Test case for valid post request to save module data
        """
        data = {
            'module_name': 'Software Engineering',
            'module_credits': 40,
            'module_level': 'L6',
            'semester': 'Double Semester',
            'delivery_language': 'English',
            'module_leader': self.user.id
        }

        self.run_valid_post_view(self.url, data)

        # test that the module has not been updated and
        # that changes do exist.

        module = Module.objects.get(module_code='CM3301')

        # check that title has changed
        self.assertEquals(module.module_name, data['module_name'])
        self.assertEquals(module.module_leader, self.user)

    def test_invalid_post_with_some_empty_data(self):
        """
        Test case for empty data in post request
        """
        data = {
            'module_name': '',
            'module_credits': 40,
            'module_level': '',
            'semester': 'Double Semester',
            'delivery_language': 'English',
            'module_leader': self.user.id
        }

        expected_validation_err = "['This field is required.']"

        context = self.run_invalid_post_view(self.url, data).context
        form_errors = context['form'].errors.as_data()

        # get the errors based on the empty values
        name_err = form_errors['module_name'][0].__str__()
        level_err = form_errors['module_level'][0].__str__()

        # test we got the expected validation error
        self.assertEquals(name_err, expected_validation_err)
        self.assertEquals(level_err, expected_validation_err)

    def test_invalid_post_with_incorrect_module_credits(self):
        """
        Test case to ensure that credits cannot go above or
        below the restrictions that are defined in model.
        """
        # data with a large module credits value
        data1 = {
            'module_code': 'CM3302',
            'module_name': 'Software Engineering Project',
            'module_credits': 2000,
            'module_level': 'L3',
            'semester': 'Double Semester',
            'delivery_language': 'English',
            'module_leader': self.user.id
        }

        # data for testing zero credits
        data2 = {
            'module_code': 'CM3302',
            'module_name': 'Software Engineering Project',
            'module_credits': 0,
            'module_level': 'L3',
            'semester': 'Double Semester',
            'delivery_language': 'English',
            'module_leader': self.user.id
        }

        # data from testing negative credits
        data3 = {
            'module_code': 'CM3302',
            'module_name': 'Software Engineering Project',
            'module_credits': -20,
            'module_level': 'L3',
            'semester': 'Double Semester',
            'delivery_language': 'English',
            'module_leader': self.user.id
        }

        less_than_data_set = [data2, data3]

        # data 1 test
        # expected error for data1
        err = "['Ensure this value is less than or equal to 120.']"

        context = self.run_invalid_post_view(self.url, data1).context
        # test large number of credits is not valid
        form_errors = context['form'].errors.as_data()
        credits_err = form_errors['module_credits'][0].__str__()
        self.assertEquals(credits_err, err)

        # since data2 and data3 are less than expected value
        # both will provide the same error
        for data in less_than_data_set:
            err = "['Ensure this value is greater than or equal to 10.']"

            context = self.run_invalid_post_view(self.url, data).context
            # test large number of credits is not valid
            form_errors = context['form'].errors.as_data()
            credits_err = form_errors['module_credits'][0].__str__()
            self.assertEquals(credits_err, credits_err)
