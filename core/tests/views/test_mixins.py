from django.test import RequestFactory
from django.views.generic import TemplateView
from django.core.urlresolvers import reverse, reverse_lazy

from core.tests.common_test_utils import LoggedInTestCase
from core.views.mixins import (AdminTestMixin, LoggedInTestMixin,
                               UserOnlyMixin)


class MockView1(AdminTestMixin, TemplateView):
        """
        Mock view that is used for AdminTestMixin
        """
        template_name = 'core/base.html'


class MockView2(LoggedInTestMixin, TemplateView):
    """
    Mock view that is used for LoggedInTestMixinTest
    """
    template_name = 'core/base.html'


class MockView3(UserOnlyMixin, TemplateView):
    template_name = 'core/base.html'


class AdminTestMixinTest(LoggedInTestCase):
    """
    Test case for testing AdminTestMixinTest
    """

    def setUp(self):
        super(AdminTestMixinTest, self).setUp()
        # set up view and request object
        self.view = MockView1()
        self.factory = RequestFactory()

    def test_admin_dispatch_logged_in_user(self):
        """
        Test if a valid admin with continue as expected
        with reques.
        """
        request = self.factory.get(reverse('dashboard'))
        request.user = self.admin
        response = MockView1.as_view()(request)
        self.assertEqual(response.status_code, 200)

    def test_admin_dispatch_non_logged_in_user(self):
        """
        Test if a not logged in, then redirect to
        login view.
        """
        request = self.factory.get(reverse('dashboard'))
        response = MockView1.as_view()(request)
        # check we are being redirected
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse_lazy('login'))

    def test_admin_dispatch_logged_in_user_wrong_permissions(self):
        """
        Test user has wrong permissions then they
        are redirect to dashboard.
        """
        request = self.factory.get(reverse('dashboard'))
        request.user = self.user
        response = MockView1.as_view()(request)
        # check we are being redirected
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse_lazy('dashboard'))


class LoggedInTestMixinTest(LoggedInTestCase):
    """
    Test case for LoggedInTestMixinTest mixin
    """

    def setUp(self):
        super(LoggedInTestMixinTest, self).setUp()
        # set up view and request object
        self.view = MockView2()
        self.factory = RequestFactory()

    def test_logged_dispatch_logged_in_user(self):
        """
        Test that if we are logged in, then we are
        redirected to dashboard.
        """
        request = self.factory.get(reverse('dashboard'))
        request.user = self.admin
        response = MockView2.as_view()(request)
        # check we are being redirected
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse_lazy('dashboard'))

    def test_logged_dispatch_non_logged_in_user(self):
        """
        Test that if we are not logged in, then
        we are directed to the login.
        """
        request = self.factory.get(reverse('dashboard'))
        response = MockView2.as_view()(request)
        # check we are being redirected
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse_lazy('login'))


class UserOnlyMixinTest(LoggedInTestCase):
    """
    Test case for testing the UserOnlyMixin
    """
    def setUp(self):
        super(UserOnlyMixinTest, self).setUp()
        self.view = MockView3()
        self.factory = RequestFactory()

    def test_user_only_success(self):
        """
        Test to check the mixin does not redirect if correct
        information is provided.
        """
        request = self.factory.get(reverse('user_settings', kwargs={
            'slug': self.admin.username}))
        request.user = self.admin
        response = MockView3.as_view()(request, slug=self.admin.username)

        self.assertEqual(response.status_code, 200)

    def test_user_only_unsuccessful(self):
        """
        Test to check that the redirect works if the slug does
        not match the current user.
        """
        request = self.factory.get(reverse('user_settings', kwargs={
            'slug': "test"}))
        request.user = self.admin
        response = MockView3.as_view()(request, slug="test")

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('dashboard'))

    def test_user_only_no_slug(self):
        """
        Test to check that no slug will redirect to dashboard.
        Unlikely to occur as urls will prevent this from happining,
        though support has been provided.
        """
        request = self.factory.get(reverse('user_settings', kwargs={
            'slug': self.admin.username}))
        request.user = self.admin
        response = MockView3.as_view()(request)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('dashboard'))

    def test_user_only_no_user(self):
        """
        Test to check that user who is not logged in is redirected
        to login form.
        """
        request = self.factory.get(reverse('user_settings', kwargs={
            'slug': "test"}))
        response = MockView3.as_view()(request, slug="test")

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('login'))
