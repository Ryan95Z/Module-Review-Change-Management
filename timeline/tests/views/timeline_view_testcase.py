from django.urls import reverse
from core.tests.common_test_utils import BaseViewTestCase, ModuleTestCase
from timeline.models import TimelineEntry


class TimelineViewTestCase(BaseViewTestCase, ModuleTestCase):
    """
    Base Test case for testing the views in the timeline package.
    Inheirts the BaseViewTestCase and ModuleTestCase classes.
    """
    def setUp(self):
        super(TimelineViewTestCase, self).setUp()

        self.admin_password = "password"

        # set up the session
        session = self.client.session
        session['username'] = self.admin.username
        session.save()

        # create an example entry for the timeline
        self.entry = TimelineEntry.objects.create(
            title="Test Changes",
            changes="Test changes to report",
            status="Draft",
            entry_type="Generic",
            module=self.module,
            approved_by=self.user
        )

    def run_get_view(self, url):
        """
        Test for getting the view successfully.
        Returns response object from view
        """
        self.client.login(
            username=self.admin.username,
            password=self.admin_password
        )
        response = self.client.get(self.url)
        self.assertEquals(response.status_code, 200)
        return response

    def run_get_view_incorrect_access(self, url):
        """
        Test returns true regardless as any user can
        view the content of this package
        """
        return True

    def run_get_view_not_logged_in(self, url):
        """
        Test to check that non-logged in users cannot access the view.
        Returns response object from view
        """
        next_url = reverse('login') + ("?next=" + url)
        response = self.client.get(url)
        self.assertEquals(response.status_code, 302)
        self.assertEquals(response.url, next_url)
        return response

    def run_valid_post_view(self, url, data):
        """
        Test for posting valid data.
        Returns response object from view
        """
        self.client.force_login(self.admin)
        response = self.client.post(url, data)
        self.assertEquals(response.status_code, 302)
        return response

    def run_invalid_post_view(self, url, data):
        """
        Test for posting invalid data.
        Returns response object from view
        """
        self.client.force_login(self.admin)
        response = self.client.post(url, data)
        self.assertEquals(response.status_code, 200)
        return response
