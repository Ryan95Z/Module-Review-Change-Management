from django.test import RequestFactory
from django.views.generic import TemplateView
from django.core.urlresolvers import reverse

from core.tests.common_test_utils import LoggedInTestCase
from core.views.mixins import AdminTestMixin


class MockView(AdminTestMixin, TemplateView):
        """
        Mock view that is used for AdminTestMixin
        """
        template_name = 'core/base.html'


class AdminTestMixinTest(LoggedInTestCase):
    """
    Test case for testing AdminTestMixinTest
    """

    def setUp(self):
        super(AdminTestMixinTest, self).setUp()
        # set up view and request object
        self.view = MockView
        self.factory = RequestFactory()

    def test_admin_dispatch_logged_in_user(self):
        """
        Test if a valid admin with continue as expected
        with reques.
        """
        request = self.factory.get(reverse('dashboard'))
        request.user = self.admin
        response = self.view.as_view()(request)
        self.assertEqual(response.status_code, 200)

    def test_admin_dispatch_non_logged_in_user(self):
        """
        Test if a not logged in, then redirect to
        login view.
        """
        request = self.factory.get(reverse('dashboard'))
        response = self.view.as_view()(request)
        # check we are being redirected
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('login'))

    def test_admin_dispatch_logged_in_user_wrong_permissions(self):
        """
        Test user has wrong permissions then they
        are redirect to dashboard.
        """
        request = self.factory.get(reverse('dashboard'))
        request.user = self.user
        response = self.view.as_view()(request)
        # check we are being redirected
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('dashboard'))
