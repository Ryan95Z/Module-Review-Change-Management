from django.test import RequestFactory
from django.views.generic import TemplateView
from django.core.urlresolvers import reverse, reverse_lazy

from core.tests.logged_in_test_case import LoggedInTestCase
from core.views.mixins import (AdminTestMixin, LoggedInTestMixin)

class MockView1(AdminTestMixin, TemplateView):
		template_name ='core/base.html'


class MockView2(LoggedInTestMixin, TemplateView):
	template_name ='core/base.html'


class AdminTestMixinTest(LoggedInTestCase):

	def setUp(self):
		super(AdminTestMixinTest, self).setUp()
		self.view = MockView1()
		self.factory = RequestFactory()

	def test_admin_dispatch_logged_in_user(self):
		request = self.factory.get(reverse('dashboard'))
		request.user = self.admin
		response = MockView1.as_view()(request)
		self.assertEqual(response.status_code, 200)

	def test_admin_dispatch_non_logged_in_user(self):
		request = self.factory.get(reverse('dashboard'))
		response = MockView1.as_view()(request)
		self.assertEqual(response.status_code, 302)
		self.assertEqual(response.url, reverse_lazy('login'))

	def test_admin_dispatch_logged_in_user_wrong_permissions(self):
		request = self.factory.get(reverse('dashboard'))
		request.user = self.user
		response = MockView1.as_view()(request)
		self.assertEqual(response.status_code, 302)
		self.assertEqual(response.url, reverse_lazy('dashboard'))

class LoggedInTestMixinTest(LoggedInTestCase):
	def setUp(self):
		super(LoggedInTestMixinTest, self).setUp()
		self.view = MockView2()
		self.factory = RequestFactory()

	def test_logged_dispatch_logged_in_user(self):
		request = self.factory.get(reverse('dashboard'))
		request.user = self.admin
		response = MockView2.as_view()(request)
		self.assertEqual(response.status_code, 302)
		self.assertEqual(response.url, reverse_lazy('dashboard'))

	def test_logged_dispatch_non_logged_in_user(self):
		request = self.factory.get(reverse('dashboard'))
		response = MockView2.as_view()(request)
		self.assertEqual(response.status_code, 302)
		self.assertEqual(response.url, reverse_lazy('login'))