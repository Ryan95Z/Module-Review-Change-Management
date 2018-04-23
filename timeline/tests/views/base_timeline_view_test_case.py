from django.core.urlresolvers import reverse
from core.tests.common_test_utils import BaseViewTestCase, ModuleTestCase


class BaseTimelineViewTestCase(BaseViewTestCase, ModuleTestCase):
    """
    Base Test case for the timeline views
    """
    def setUp(self):
        super(BaseTimelineViewTestCase, self).setUp()
        session = self.client.session
        session['username'] = self.admin.username
        session.save()

        self.admin_password = "password"

    def run_get_view(self, url):
        """
        view test for getting the view successfully.
        Returns response object from view
        """
        self.client.login(
            username=self.admin.username,
            password=self.admin_password
        )
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
        return response

    def run_get_method_not_allows(self, url):
        self.client.login(
            username=self.admin.username,
            password=self.admin_password
        )
        response = self.client.get(url)
        self.assertEquals(response.status_code, 405)
        return response

    def run_get_view_incorrect_access(self, url):
        """
        view test for checking non-admins cannot
        access the view.
        Returns response object from view
        """
        self.client.force_login(self.user)
        response = self.client.get(url)
        self.assertEquals(response.status_code, 302)
        self.assertEquals(response.url, reverse('dashboard'))
        return response

    def run_get_view_not_logged_in(self, url):
        """
        view test to check that non-logged in users
        can access the view.
        Returns response object from view
        """
        next_url = reverse('login') + ("?next=" + url)
        response = self.client.get(url)
        self.assertEquals(response.status_code, 302)
        self.assertEquals(response.url, next_url)
        return response

    def run_valid_post_view(self, url, data):
        """
        view test for posting valid data.
        Returns response object from view
        """
        self.client.force_login(self.admin)
        response = self.client.post(url, data)
        self.assertEquals(response.status_code, 302)
        return response

    def run_valid_post_view_no_redirect(self, url, data):
        """
        view test for posting valid data.
        Returns response object from view
        """
        self.client.force_login(self.admin)
        response = self.client.post(url, data)
        self.assertEquals(response.status_code, 200)
        return response

    def run_valid_ajax(self, url, data):
        self.client.force_login(self.admin)
        response = self.client.post(
            url,
            data,
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertEquals(response.status_code, 200)
        return response

    def run_post_not_allowed(self, url, data):
        self.client.force_login(self.admin)
        response = self.client.post(url, data)
        self.assertEquals(response.status_code, 405)
        return response

    def run_invalid_post_view(self, url, data):
        """
        view test for posting invalid data.
        Returns response object from view
        """
        self.client.force_login(self.admin)
        response = self.client.post(url, data)
        self.assertEquals(response.status_code, 200)
        return response
