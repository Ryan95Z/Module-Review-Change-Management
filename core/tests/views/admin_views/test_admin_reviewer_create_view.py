from django.core.urlresolvers import reverse
from core.tests.common_test_utils import LoggedInTestCase
from core.models import Module, UserManager, User

class ReviewerCreateViewTests(LoggedInTestCase):
    def setUp(self):
        super(ReviewerCreateViewTests, self).setUp()

        # update admin user permissons for this test
        self.admin.is_module_reviewer = True
        self.admin.save()

        self.url = reverse('new_reviewer')
        session = self.client.session
        session['username'] = self.admin.username
        session.save()

        user_model = User
        # Create a user to be a module leader for the test module
        self.module_leader = user_model.objects.create(
            username="leader",
            first_name="Module",
            last_name="Leader",
            email="ml@test.com",
            password="password"
        )

        # Create a test module
        module_model = Module
        self.test_module = module_model.objects.create(
            module_code = "CM1101",
            module_name = "Test Module",
            module_credits = "10",
            module_level = "1",
            module_year = "1",
            semester = "Autumn Semester",
            delivery_language = "English",
            module_leader = self.module_leader
        )

    def test_get_reviewer_create_view(self):
        """
        We should only be able to access the view as admin
        """
        login = self.client.login(username="admin", password="password")
        response = self.client.get(self.url)
        context = response.context

        self.assertEquals(response.status_code, 200)
        self.assertEquals(context['form_url'], self.url)
        self.assertEquals(context['form_type'], 'Create')

    def test_get_reviewer_create_view_with_incorrect_access(self):
        """
        We shouldn't be able to access the view when not admin
        """
        self.client.force_login(self.user)
        response = self.client.get(self.url)
        self.assertEquals(response.status_code, 302)
        self.assertEquals(response.url, reverse('dashboard'))

    def test_get_reviewer_create_view_not_logged_in(self):
        """
        We shouldn't be able to access the view when logged out
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
            'module': self.test_module.module_code,
            'reviewer_user': self.admin.id
        }

        self.client.force_login(self.admin)
        response = self.client.post(self.url, data)
        self.assertEquals(response.status_code, 302)
        self.assertEquals(response.url, reverse('all_reviewers'))

    def test_invalid_post_create_view(self):
        """
        Test request to check that invalid data is not processed
        """
        data = {
            'module': 1101,
            'reviewer_user': self.admin.username
        }

        self.client.force_login(self.admin)
        response = self.client.post(self.url, data)
        context = response.context
        self.assertEquals(response.status_code, 200)
        self.assertEquals(context['form_type'], 'Create')