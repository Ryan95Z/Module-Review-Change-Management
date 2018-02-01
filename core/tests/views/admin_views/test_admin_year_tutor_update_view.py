from django.core.urlresolvers import reverse
from core.tests.views.admin_views.admin_test_case import AdminViewTestCase
from core.models import YearTutor, YearTutorManager


class AdminYearTutorUpdateViewTest(AdminViewTestCase):
    """
    Test case for Admin Year Tutor Update View
    """

    # status code: 200 - Invalid form so user is direct back to it
    # status code: 302 - Form valid and user is re-directed

    def setUp(self):
        super(AdminYearTutorUpdateViewTest, self).setUp()
        # create a sample year tutor for tests
        self.manager = YearTutorManager()
        self.manager.model = YearTutor
        self.tutor = self.manager.create_tutor('Year 1', self.user)
        kwargs = {'pk': self.tutor.pk}
        self.url = reverse('update_tutor', kwargs=kwargs)

    def test_get_tutor_update_view(self):
        """
        Test case for getting the view
        """
        self.client.login(
            username=self.admin.username,
            password=self.admin_password
        )
        response = self.client.get(self.url)
        self.assertEquals(response.status_code, 200)

    def test_get_tutor_update_view_incorrect_access(self):
        """
        Test case on accessing the view with incorrect access
        """
        self.client.force_login(self.user)
        response = self.client.get(self.url)
        self.assertEquals(response.status_code, 302)
        self.assertEquals(response.url, reverse('dashboard'))

    def test_get_tutor_update_view_not_logged_in(self):
        """
        Test case for user that is not logged in when
        acessing the view.
        """
        next_url = reverse('login') + ("?next=" + self.url)
        response = self.client.get(self.url)
        self.assertEquals(response.status_code, 302)
        self.assertEquals(response.url, next_url)

    def test_valid_post_update_view(self):
        """
        Test case for a valid post request
        """
        data = {
            'tutor_year': "Year 2",
            'year_tutor_user': self.user.id
        }

        self.client.force_login(self.admin)
        response = self.client.post(self.url, data)
        self.assertEquals(response.status_code, 302)
        self.assertEquals(response.url, reverse('all_tutors'))

        updated_tutor = YearTutor.objects.get(id=self.tutor.pk)

        # make sure they are the same objects
        self.assertEquals(updated_tutor.pk, self.tutor.pk)
        # assert that the year was updated
        self.assertEquals(data['tutor_year'], updated_tutor.tutor_year)

    def test_valid_post_with_tutor_already_assigned(self):
        """
        Test case for asserting what happens if a year tutor
        is re-assigned when they have a year already applied to them.
        """
        tutor_err = "['Year tutor with this Year tutor user already exists.']"
        # create a tmp tutor to test that an already assigned
        # tutor cannot be overwritten
        tmp_tutor = self.manager.create_new_tutor(
            tutor_year="Year 2",
            username="Tutor",
            first_name="Tutor",
            last_name="Tutor",
            email="tutor@test.com",
            password="password"
        )

        data = {
            'tutor_year': "Year 2",
            'year_tutor_user': self.user.id
        }

        self.client.force_login(self.admin)
        # adjust request url to fit tmp_tutor
        response = self.client.post(
            reverse('update_tutor', kwargs={'pk': tmp_tutor.pk}),
            data
        )

        context = response.context
        # get errors from context
        form_errors = context['form'].errors.as_data()
        form_tutor_error = form_errors['year_tutor_user'][0].__str__()

        self.assertEquals(response.status_code, 200)
        self.assertEquals(context['form_type'], 'Update')
        self.assertEquals(form_tutor_error, tutor_err)

    def test_invalid_post_with_blank_data(self):
        """
        Test case for a blank data
        """
        required_error = "['This field is required.']"
        data = {
            'tutor_year': '',
            'year_tutor_user': ''
        }

        self.client.force_login(self.admin)
        response = self.client.post(self.url, data)

        context = response.context
        # get the errors from the view context
        form_errors = context['form'].errors.as_data()
        form_tutor_year_error = form_errors['tutor_year'][0].__str__()
        form_tutor_error = form_errors['year_tutor_user'][0].__str__()

        self.assertEquals(response.status_code, 200)
        self.assertEquals(context['form_type'], 'Update')
        self.assertEquals(form_tutor_error, required_error)
        self.assertEquals(form_tutor_year_error, required_error)

    def test_invalid_post_with_random_data(self):
        """
        Test case for invalid data is not processed
        """
        data = {
            'tutor_year': "1234",
            'year_tutor_user': self.admin.username
        }

        self.client.force_login(self.admin)
        response = self.client.post(self.url, data)
        self.assertEquals(response.status_code, 200)
