from django.core.urlresolvers import reverse
from core.tests.views.admin_views.admin_test_case import AdminViewTestCase
from core.models import ProgrammeTutorManager, ProgrammeTutor, User


class AdminYearTutorCreateViewTest(AdminViewTestCase):
    """
    Test case for AdminYearTutorCreateView
    """
    def setUp(self):
        super(AdminYearTutorCreateViewTest, self).setUp()
        self.url = reverse('new_tutor')

        # update admin user permissons for this test
        self.admin.is_year_tutor = True
        self.admin.save()

    def test_get_tutor_create_view(self):
        """
        Test case for accessing the view
        """
        response = self.run_get_view(self.url)
        context = response.context

        self.assertEquals(context['form_url'], self.url)
        self.assertEquals(context['form_type'], 'Create')

    def test_get_tutor_create_view_with_incorrect_access(self):
        """
        Test case for checking non-admin users can access view
        """
        self.run_get_view_incorrect_access(self.url)

    def test_get_tutor_create_view_not_logged_in(self):
        """
        Test case for non-logged in user
        """
        self.run_get_view_not_logged_in(self.url)

    def test_valid_post_create_view(self):
        """
        Test of valid create view
        """
        data = {
            'programme_name': 'Computer Science',
            'tutor_year': "Year 1",
            'programme_tutor_user': self.admin.id
        }

        response = self.run_valid_post_view(self.url, data)
        self.assertEquals(response.url, reverse('all_tutors'))

    def test_valid_post_with_exsiting_user(self):
        """
        Test case for ensuring user cannot be applied to
        further years
        """
        manager = ProgrammeTutorManager()
        manager.model = ProgrammeTutor

        # create a tutor
        tutor = manager.create_tutor('Computer Science', 'Year 1', self.user)

        tutor_err = "['Programme tutor with this Programme tutor user already exists.']"

        # attempt to add user ad a tutor again
        data = {
            'programme_name': 'Computer Science',
            'tutor_year': "Year 2",
            'programme_tutor_user': self.user.id
        }

        context = self.run_invalid_post_view(self.url, data).context
        self.assertEquals(context['form_type'], 'Create')

        # check that an error was provided
        form_errors = context['form'].errors.as_data()
        tutor_error = form_errors['programme_tutor_user'][0].__str__()
        self.assertEquals(tutor_error, tutor_err)

    def test_invalid_post_create_view(self):
        """
        Test request to check that invalid data is not processed
        """
        data = {
            'programme_name': 'Computer Science',
            'tutor_year': 1,
            'programme_tutor_user': self.admin.username
        }

        context = self.run_invalid_post_view(self.url, data).context
        self.assertEquals(context['form_type'], 'Create')
