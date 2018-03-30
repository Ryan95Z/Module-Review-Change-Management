from django.core.urlresolvers import reverse
from core.tests.views.admin_views.admin_test_case import AdminViewTestCase
from core.models import ProgrammeTutor, ProgrammeTutorManager, Module


class AdminProgrammeTutorUpdateViewTest(AdminViewTestCase):
    """
    Test case for Admin Programme Tutor Update View
    """

    # status code: 200 - Invalid form so user is direct back to it
    # status code: 302 - Form valid and user is re-directed

    def setUp(self):
        super(AdminProgrammeTutorUpdateViewTest, self).setUp()

        # create a sample programme tutor for tests
        self.manager = ProgrammeTutorManager()
        self.manager.model = ProgrammeTutor
        self.tutor = self.manager.create_tutor(
            'Compuyter Science', 'Year 1', self.user)

        kwargs = {'pk': self.tutor.pk}
        self.url = reverse('update_tutor', kwargs=kwargs)

        self.admin.is_module_leader = True
        self.admin.save()

        self.module = Module.objects.create(
            module_code="CMXXXX",
            module_name="Test Module",
            module_credits="10",
            module_level="L4",
            semester="Autumn Semester",
            delivery_language="English",
            module_leader=self.admin
        )

    def test_get_tutor_update_view(self):
        """
        Test case for getting the view
        """
        self.run_get_view(self.url)

    def test_get_tutor_update_view_incorrect_access(self):
        """
        Test case on accessing the view with incorrect access
        """
        self.run_get_view_incorrect_access(self.url)

    def test_get_tutor_update_view_not_logged_in(self):
        """
        Test case for user that is not logged in when
        acessing the view.
        """
        self.run_get_view_not_logged_in(self.url)

    def test_valid_post_update_view(self):
        """
        Test case for a valid post request
        """
        data = {
            'programme_name': "Computer Science",
            'tutor_year': "Year 1",
            'modules': self.module.module_code
        }

        response = self.run_valid_post_view(self.url, data)

        self.client.force_login(self.admin)
        response = self.client.post(self.url, data)

        self.assertEquals(response.url, reverse('all_tutors'))

        updated_tutor = ProgrammeTutor.objects.get(id=self.tutor.pk)

        # make sure they are the same objects
        self.assertEquals(updated_tutor.pk, self.tutor.pk)

        # assert that the year was updated
        self.assertEquals(data['tutor_year'], updated_tutor.tutor_year)

    def test_invalid_post_with_blank_data(self):
        """
        Test case for a blank data
        """
        required_error = "['This field is required.']"
        data = {
            'programme_name': '',
            'tutor_year': '',
        }

        context = self.run_invalid_post_view(self.url, data).context

        # get the errors from the view context
        form_errors = context['form'].errors.as_data()
        form_tutor_name_error = form_errors['programme_name'][0].__str__()
        form_tutor_year_error = form_errors['tutor_year'][0].__str__()

        self.assertEquals(context['form_type'], 'Update')
        self.assertEquals(form_tutor_name_error, required_error)
        self.assertEquals(form_tutor_year_error, required_error)

    def test_invalid_post_with_random_data(self):
        """
        Test case for invalid data is not processed
        """
        data = {
            'programme_name': 34,
            'tutor_year': "1234",
        }

        self.run_invalid_post_view(self.url, data)
