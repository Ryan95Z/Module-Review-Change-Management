from django.core.urlresolvers import reverse
from core.tests.views.admin_views.admin_test_case import AdminViewTestCase
from core.tests.common_test_utils import ModuleTestCase
from core.models import Reviewer, ReviewerManager


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
            'modules': [self.module.pk, self.module_two.pk]
        }

        response = self.run_valid_post_view(self.url, data)
        self.assertEquals(response.url, reverse('all_reviewers'))

        updated_reviewer = Reviewer.objects.get(id=self.reviewer.pk)
        self.assertEquals(updated_reviewer, self.reviewer)

    def test_invalid_post_with_random_data(self):
        """
        Test case for invalid data is not processed
        """
        data = {
            'user': "hello",
            'modules': self.module
        }

        self.run_invalid_post_view(self.url, data)
