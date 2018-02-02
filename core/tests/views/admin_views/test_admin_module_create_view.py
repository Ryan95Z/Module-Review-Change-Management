from django.core.urlresolvers import reverse
from core.tests.views.admin_views.admin_test_case import AdminViewTestCase
from core.models import Module


class AdminTestModuleCreateView(AdminViewTestCase):

    def setUp(self):
        super(AdminTestModuleCreateView, self).setUp()
        self.url = reverse('new_module')

    def test_get_module_create_view(self):
        """
        Test case for accessing the view
        """
        response = self.run_get_view(self.url)
        context = response.context

        self.assertEquals(context['form_url'], self.url)
        self.assertEquals(context['form_type'], 'Create')

    def test_get_module_create_view_with_incorrect_access(self):
        """
        Test case for checking non-admin users can access view
        """
        self.run_get_view_incorrect_access(self.url)

    def test_get_module_create_view_not_logged_in(self):
        """
        Test case for non-logged in user
        """
        self.run_get_view_not_logged_in(self.url)

    def test_valid_post_create_view(self):
        data = {
            'module_code': 'CM3301',
            'module_name': 'Software Engineering Project',
            'module_credits': 40,
            'module_level': 'L3',
            'module_year': 'Year 3',
            'semester': 'Autumn Semester',
            'delivery_language': 'English',
            'module_leader': self.user.id
        }

        self.run_valid_post_view(self.url, data)

        # test some of the data matches the model once it has been created
        module = Module.objects.get(module_code='CM3301')
        self.assertEquals(module.module_code, data['module_code'])
        self.assertEquals(module.module_name, data['module_name']),
        self.assertEquals(module.module_leader, self.user)

    def test_invalid_post_create_view(self):
        """
        Test case for invalid data to the post request
        """
        data = {
            'module_code': '',
            'module_name': 'Software Engineering Project',
            'module_credits': '10 Credits',
            'module_level': 'L3',
            'module_year': 'Year 3',
            'semester': 'Autumn Semester',
            'delivery_language': 'English',
            'module_leader': self.user.id
        }

        # expected validation errors from above data
        credits_err = "['Enter a whole number.']"
        code_err = "['This field is required.']"

        response = self.run_invalid_post_view(self.url, data)

        # assert that errors are provided if some data is invalid
        form_errors = response.context['form'].errors.as_data()
        form_credits_err = form_errors['module_credits'][0].__str__()
        form_code_err = form_errors['module_code'][0].__str__()

        self.assertEquals(form_code_err, code_err)
        self.assertEquals(form_credits_err, credits_err)
