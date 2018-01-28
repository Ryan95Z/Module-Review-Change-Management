from django.test import RequestFactory
from django.views.generic import TemplateView
from django.core.urlresolvers import reverse

from core.tests.common_test_utils import LoggedInTestCase
from core.views.mixins import LoggedInTestMixin


class MockView(LoggedInTestMixin, TemplateView):
    """
    Mock view that is used for LoggedInTestMixinTest
    """
    template_name = 'core/base.html'


class LoggedInTestMixinTest(LoggedInTestCase):
    """
    Test case for LoggedInTestMixinTest mixin
    """

    def setUp(self):
        super(LoggedInTestMixinTest, self).setUp()
        # set up view and request object
        self.view = MockView
        self.factory = RequestFactory()

    def test_logged_dispatch_logged_in_user(self):
        """
        Test that if we are logged in, then we are
        redirected to dashboard.
        """
        request = self.factory.get(reverse('dashboard'))
        request.user = self.admin
        response = self.view.as_view()(request)
        # check we are being redirected
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('dashboard'))

    def test_logged_dispatch_non_logged_in_user(self):
        """
        Test that if we are not logged in, then
        we are directed to the login.
        """
        request = self.factory.get(reverse('dashboard'))
        response = self.view.as_view()(request)
        # check we are being redirected
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('login'))
