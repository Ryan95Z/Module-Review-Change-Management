from django.core.urlresolvers import reverse_lazy
from core.tests.logged_in_test_case import LoggedInTestCase

class LoginViewTest(LoggedInTestCase):
	def setUp(self):
		super(LoginViewTest, self).setUp()

	def test_get_user_login_view(self):
		response = self.client.get(reverse_lazy('login'))
		self.assertEquals(response.status_code, 200)

	def test_get_user_login_view_logged_in_already(self):
		self.client.force_login(self.user)
		response = self.client.get(reverse_lazy('login'))
		self.assertEquals(response.status_code, 302)
		self.assertEquals(response.url, reverse_lazy('dashboard'))

	def test_post_user_login_view_valid_details(self):
		data = {'username' : 'admin', 'password' : 'password'}
		response = self.client.post(reverse_lazy('login'), data)
		self.assertEquals(response.status_code, 302)
		self.assertEquals(response.url, reverse_lazy('dashboard'))

	def test_post_user_login_view_invalid_details(self):
		data = {'username' : 'admin', 'password' : 'badpassword'}
		response = self.client.post(reverse_lazy('login'), data)
		self.assertEquals(response.status_code, 302)
		self.assertEquals(response.url, reverse_lazy('login'))

	def test_post_user_login_view_blank_details(self):
		data = {'username' : '', 'password' : ''}
		response = self.client.post(reverse_lazy('login'), data)
		self.assertEquals(response.status_code, 302)
		self.assertEquals(response.url, reverse_lazy('login'))

	def test_post_user_login_view_logged_in_already(self):
		self.client.force_login(self.user)
		data = {'username' : 'admin', 'password' : 'password'}
		response = self.client.post(reverse_lazy('login'), data)
		self.assertEquals(response.status_code, 302)
		self.assertEquals(response.url, reverse_lazy('dashboard'))


class LogoutViewTest(LoggedInTestCase):
	def test_get_user_logout_view(self):
		self.client.force_login(self.user)
		response = self.client.get(reverse_lazy('logout'))
		self.assertEquals(response.status_code, 302)
		self.assertEquals(response.url, reverse_lazy('login'))

	def test_get_user_logout_view_not_logged_in(self):
		response = self.client.get(reverse_lazy('logout'))
		self.assertEquals(response.status_code, 302)
		self.assertEquals(response.url, reverse_lazy('login'))


class UserListViewTest(LoggedInTestCase):
	def setUp(self):
		super(UserListViewTest, self).setUp()

	def test_get_user_list_view(self):
		self.client.force_login(self.admin)
		response = self.client.get(reverse_lazy('all_users'))
		self.assertEquals(response.status_code, 200)

	def test_get_user_list_view_with_incorrect_access(self):
		self.client.force_login(self.user)
		response = self.client.get(reverse_lazy('all_users'))
		self.assertEquals(response.status_code, 302)
		self.assertEquals(response.url, reverse_lazy('dashboard'))

	def test_get_user_list_view_not_logged_in(self):
		response = self.client.get(reverse_lazy('all_users'))
		self.assertEquals(response.status_code, 302)
		self.assertEquals(response.url, reverse_lazy('login'))