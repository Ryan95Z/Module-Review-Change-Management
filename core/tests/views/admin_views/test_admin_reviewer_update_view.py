from django.core.urlresolvers import reverse
from core.tests.views.admin_views.admin_test_case import AdminViewTestCase
from core.tests.common_test_utils import ModuleTestCase
from core.models import Reviewer, ReviewerManager, Module

class AdminReviewerUpdateViewTests(AdminViewTestCase, ModuleTestCase):
    def setUp(self):
        super(AdminReviewerUpdateViewTests, self).setUp()
        self.manager = ReviewerManager()
        self.manager.model = Reviewer
        self.reviewer = self.manager.create_reviewer(self.module, self.user)
        kwargs = {'pk': self.reviewer.pk}
        self.url = reverse('update_reviewer', kwargs=kwargs)

    def test_get_reviewer_update_view(self):
        """
        Get the view
        """
        self.run_get_view(self.url)

    def test_get_reviewer_update_incorrect_access(self):
        """
        Get the view with incorrect access
        """
        self.run_get_view_incorrect_access(self.url)
    
    def test_get_reviewer_update_view_not_logged_in(self):
        """
        Get the view when not logged in
        """
        self.run_get_view_not_logged_in(self.url)

    def test_valid_post_with_single_module(self):
        """
        Valid post request with a single module
        """
        data = {
            'user': self.user.pk,
            'modules': self.module.pk
        }

        response = self.run_valid_post_view(self.url, data)
        self.assertEquals(response.url, reverse('all_reviewers'))

        updated_reviewer = Reviewer.objects.get(id=self.reviewer.pk)
        self.assertEquals(updated_reviewer, self.reviewer)
    
    def test_valid_post_with_multiple_modules(self):
        """
        Valid post request with multiple modules
        """
        data = {
            'user': self.user.pk,
            'modules': [self.module.pk, self.module_two.pk]
        }

        response = self.run_valid_post_view(self.url, data)
        self.assertEquals(response.url, reverse('all_reviewers'))

        updated_reviewer = Reviewer.objects.get(id=self.reviewer.pk)
        self.assertEquals(updated_reviewer, self.reviewer)


    def test_valid_post_with_user_already_assigned(self):
        """
        Valid post, but the user is already assigned as a reviewer
        """
        reviewer_error = "['Reviewer with this User already exists.']"

        # Create second reviewer object
        new_reviewer = self.manager.create_new_reviewer(
            modules=self.module_two,
            username="newreviewer",
            first_name="new",
            last_name="reviewer",
            email="nr@example.com",
            password="password"
        )

        data = {
            'user': new_reviewer.user.pk,
            'modules': [self.module.pk]
        }

        context = self.run_invalid_post_view(self.url, data).context

        # get errors from context
        form_errors = context['form'].errors.as_data()
        form_reviewer_error = form_errors['user'][0].__str__()

        self.assertEquals(context['form_type'], 'Update')
        self.assertEquals(form_reviewer_error, reviewer_error)

    def test_invalid_post_with_random_data(self):
        """
        Test case for invalid data is not processed
        """
        data = {
            'user': "hello",
            'modules': self.module
        }

        self.run_invalid_post_view(self.url, data)