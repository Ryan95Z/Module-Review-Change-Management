from django.test import Client, TestCase
from core.models import User, UserManager

class LoggedInTestCase(TestCase):
	def setUp(self):
		super(LoggedInTestCase, self).setUp()
		self.client = Client()
		manager = UserManager()
		manager.model = User
		self.admin = manager.create_superuser(
			username='admin',
			first_name='admin',
			last_name='admin',
			email='admin@example.com',
			password='password'
		)

		self.user = manager.create_user(
			username='user1',
			first_name='user',
			last_name='user',
			email='admin@example.com',
			password='password'
		)