from django.core.urlresolvers import reverse
from core.tests.views.admin_views.admin_test_case import AdminViewTestCase
from core.models import Reviewer, ReviewerManager, Module

class ReviewerDeleteTests(AdminViewTestCase):
    """
    Tests for the the ReviewerDeleteView
    """
    def setUp(self):
        super(ReviewerDeleteTests, self).setUp()

        self.test_module = Module.objects.create(
            module_code = "CM1101",
            module_name = "Test Module",
            module_credits = "10",
            module_level = "1",
            semester = "Autumn Semester",
            delivery_language = "English",
            module_leader = self.user
        )

        self.manager = ReviewerManager()
        self.manager.model = Reviewer
        self.reviewer = self.manager.create_reviewer([self.test_module], self.user)
        kwargs = {'pk': self.reviewer.pk}
        
        self.url = reverse('delete_reviewer', kwargs=kwargs)

    def test_get_reviewer_delete_view(self):
        """
        We should be able to access the view if we
        are logged in as admin.
        """

        self.run_get_view(self.url)

    def test_get_user_delete_view_with_incorrect_access(self):
        """
        If we aren't admin, we shouldn't be able to access
        the view
        """
        self.run_get_view_incorrect_access(self.url)

    def test_get_reviewer_list_view_not_logged_in(self):
        """
        If we aren't logged in, we shouldn't be able to
        access the view
        """
        self.run_get_view_not_logged_in(self.url)

    def test_reviewer_delete_view_confirmation(self):
        """
        If we access the view with a get request, a 
        confirmation form should be shown, and the url
        should not be directed.
        """

        response = self.run_get_view(self.url)
        contains_form = False
        for template in response.templates:
            if template.name == "core/reviewer_confirm_delete.html":
                contains_form = True
                break
        self.assertTrue(contains_form)


    def test_valid_post_reviewer_delete(self):
        """
        If the view is requested with a post, the object should be deleted
        and the user should be redirected to all_reviewers
        """
        reviewer_id = self.reviewer.id
        data = {}
        response = self.run_valid_post_view(self.url, data)
        with self.assertRaises(Reviewer.DoesNotExist):
            Reviewer.objects.get(id=reviewer_id)
        self.assertEqual(response.url, reverse('all_reviewers'))