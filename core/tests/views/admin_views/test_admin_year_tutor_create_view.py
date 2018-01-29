from django.core.urlresolvers import reverse
from core.tests.common_test_utils import LoggedInTestCase
from core.models import YearTutorManager, YearTutor, User


class AdminYearTutorCreateViewTest(LoggedInTestCase):
    def setUp(self):
        super(AdminYearTutorCreateViewTest, self).setUp()
        # update admin user permissons for this test
        self.admin.is_year_tutor = True
        self.admin.save()

        self.url = reverse('new_tutor')
        session = self.client.session
        session['username'] = self.admin.username
        session.save()

    def test_get_tutor_create_view(self):
        """
        Test case for accessing the view
        """
        login = self.client.login(username="admin", password="password")
        response = self.client.get(self.url)
        context = response.context

        self.assertEquals(response.status_code, 200)
        self.assertEquals(context['form_url'], self.url)
        self.assertEquals(context['form_type'], 'Create')

    def test_get_tutor_create_view_with_incorrect_access(self):
        """
        Test case for checking non-admin users can access view
        """
        self.client.force_login(self.user)
        response = self.client.get(self.url)
        self.assertEquals(response.status_code, 302)
        self.assertEquals(response.url, reverse('dashboard'))

    def test_get_tutor_create_view_not_logged_in(self):
        """
        Test case for non-logged in user
        """
        next_url = reverse('login') + ("?next=" + self.url)
        response = self.client.get(self.url)
        self.assertEquals(response.status_code, 302)
        self.assertEquals(response.url, next_url)

    def test_valid_post_create_view(self):
        """
        Test of valid create view
        """
        data = {
            'tutor_year': "Year 1",
            'year_tutor_user': self.admin.id
        }

        self.client.force_login(self.admin)
        response = self.client.post(self.url, data)
        self.assertEquals(response.status_code, 302)
        self.assertEquals(response.url, reverse('all_tutors'))

    def test_valid_post_with_exsiting_user(self):
        """
        Test case for ensuring user cannot be applied to
        further years
        """
        manager = YearTutorManager()
        manager.model = YearTutor

        # create a tutor
        tutor = manager.create_tutor('Year 1', self.user)

        tutor_err = "['Year tutor with this Year tutor user already exists.']"

        # attempt to add user ad a tutor again
        data = {
            'tutor_year': "Year 2",
            'year_tutor_user': self.user.id
        }

        self.client.force_login(self.admin)
        response = self.client.post(self.url, data)
        context = response.context
        self.assertEquals(response.status_code, 200)
        self.assertEquals(context['form_type'], 'Create')

        # check that an error was provided
        form_errors = context['form'].errors.as_data()
        tutor_error = form_errors['year_tutor_user'][0].__str__()
        self.assertEquals(tutor_error, tutor_err)

    def test_invalid_post_create_view(self):
        """
        Test request to check that invalid data is not processed
        """
        data = {
            'tutor_year': 1,
            'year_tutor_user': self.admin.username
        }

        self.client.force_login(self.admin)
        response = self.client.post(self.url, data)
        context = response.context
        self.assertEquals(response.status_code, 200)
        self.assertEquals(context['form_type'], 'Create')
