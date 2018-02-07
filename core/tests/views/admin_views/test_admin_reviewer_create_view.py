from django.core.urlresolvers import reverse
from core.tests.views.admin_views.admin_test_case import AdminViewTestCase
from core.models import Module, UserManager, User, Reviewer

class ReviewerCreateViewTests(AdminViewTestCase):
    def setUp(self):
        super(ReviewerCreateViewTests, self).setUp()
        self.url = reverse("new_reviewer")

        # update admin user permissons for this test
        self.admin.is_module_reviewer = True
        self.admin.save()

        # Create a user to be a module leader for the test module
        self.module_leader = User.objects.create(
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
        response = self.run_get_view(self.url)
        context = response.context

        self.assertEquals(context['form_url'], self.url)
        self.assertEquals(context['form_type'], 'Create')

    def test_get_reviewer_create_view_with_incorrect_access(self):
        """
        We shouldn't be able to access the view when not admin
        """
        self.run_get_view_incorrect_access(self.url)

    def test_get_reviewer_create_view_not_logged_in(self):
        """
        We shouldn't be able to access the view when logged out
        """
        self.run_get_view_not_logged_in(self.url)
    
    def test_valid_post_create_view(self):
        """
        Test of valid create view
        """
        data = {
            'modules': self.test_module.module_code,
            'user': self.module_leader.id
        }

        response = self.run_valid_post_view(self.url, data)
        self.assertEquals(response.url, reverse('all_reviewers'))