from django.core.urlresolvers import reverse
from core.tests.common_test_utils import LoggedInTestCase

class ReviewerListViewTests(LoggedInTestCase):
    """
    Tests for the the ReviewerListView
    """
    def setUp(self):
        super(ReviewerListViewTests, self).setUp()
        self.url = reverse('all_reviewers')

    def test_get_reviewer_list_view(self):
        """
        We should be able to access the view if we
        are logged in as admin
        """
        session = self.client.session
        session['username'] = "admin"
        session.save()
        login = self.client.login(username="admin", password="password")
        response = self.client.get(self.url)
        self.assertEquals(response.status_code, 200)

    def test_get_user_list_view_with_incorrect_access(self):
        """
        If we aren't admin, we shouldn't be able to access
        the view
        """
        self.client.force_login(self.user)
        response = self.client.get(self.url)
        self.assertEquals(response.status_code, 302)
        self.assertEquals(response.url, reverse('dashboard'))

    def test_get_reviewer_list_view_not_logged_in(self):
        """
        If we aren't logged in, we shouldn't be able to
        access the view
        """
        next_url = reverse('login') + ("?next=" + self.url)
        response = self.client.get(self.url)
        self.assertEquals(response.status_code, 302)
        self.assertEquals(response.url, next_url)
    