from django.test import RequestFactory
from django.views.generic import TemplateView
from django.core.urlresolvers import reverse

from core.tests.common_test_utils import LoggedInTestCase
from core.views.mixins import UserOnlyMixin


class MockView(UserOnlyMixin, TemplateView):
    template_name = 'core/base.html'


class UserOnlyMixinTest(LoggedInTestCase):
    """
    Test case for testing the UserOnlyMixin
    """
    def setUp(self):
        super(UserOnlyMixinTest, self).setUp()
        self.view = MockView
        self.factory = RequestFactory()

    def test_user_only_success(self):
        """
        Test to check the mixin does not redirect if correct
        information is provided.
        """
        request = self.factory.get(reverse('user_settings', kwargs={
            'slug': self.admin.username}))
        request.user = self.admin
        response = self.view.as_view()(request, slug=self.admin.username)

        self.assertEqual(response.status_code, 200)

    def test_user_only_unsuccessful(self):
        """
        Test to check that the redirect works if the slug does
        not match the current user.
        """
        request = self.factory.get(reverse('user_settings', kwargs={
            'slug': "test"}))
        request.user = self.admin
        response = self.view.as_view()(request, slug="test")

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
        response = self.view.as_view()(request)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('dashboard'))

    def test_user_only_no_user(self):
        """
        Test to check that user who is not logged in is redirected
        to login form.
        """
        request = self.factory.get(reverse('user_settings', kwargs={
            'slug': "test"}))
        response = self.view.as_view()(request, slug="test")

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('login'))
