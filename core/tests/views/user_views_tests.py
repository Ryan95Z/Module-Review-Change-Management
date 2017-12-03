import unittest
from django.test import Client, TestCase
from django.core.urlresolvers import reverse_lazy

from core.models import User, UserManager

class UserListView(TestCase):
	def setUp(self):
		self.client = Client()
		manager = UserManager()
		manager.model = User
		
		manager.create_superuser(
			username='admin',
			first_name='admin',
			last_name='admin',
			email='admin@example.com',
			password='password'
		)

		manager.create_user(
			username='user1',
			first_name='user',
			last_name='user',
			email='admin@example.com',
			password='password'
		)


	def test_get_user_list_view(self):
		self.client.login(username='admin', password='password')
		response = self.client.get(reverse_lazy('all_users'))
		self.assertEquals(response.status_code, 200)

	def test_get_user_list_view_with_incorrect_access(self):
		self.client.login(username='user1', password='password')
		response = self.client.get(reverse_lazy('all_users'))
		self.assertEquals(response.status_code, 302)
		self.assertEquals(response.url, reverse_lazy('dashboard'))

	def test_get_user_list_view_not_logged_in(self):
		response = self.client.get(reverse_lazy('all_users'))
		self.assertEquals(response.status_code, 302)
		self.assertEquals(response.url, reverse_lazy('login'))
