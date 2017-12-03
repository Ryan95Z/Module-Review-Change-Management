from django.test import TestCase
from core.models import User

class UserTestCase(TestCase):
	def setUp(self):
		User.objects.create(
			username="Test",
			first_name="Test",
			last_name="Last",
			email="test@example.com"
		)

		User.objects.create(
			username="Admin",
			first_name="admin",
			last_name="admin",
			email="admin@example.com",
			is_admin=True
		)

		User.objects.create(
			username="Admin1",
			first_name="admin",
			last_name="admin",
			email="admin@example.com",
			is_admin=True,
			is_module_leader=True,
			is_office_admin=True,
			is_year_tutor=True			
		)

	def test_basic_user_details(self):
		# test basic user
		test_user = User.objects.get(username="Test")
		self.assertEqual(test_user.username, "Test")
		self.assertEqual(test_user.get_full_name(), "Test Last")
		self.assertEqual(test_user.get_short_name(), "Test")
		self.assertEqual(test_user.email, "test@example.com")
		self.assertFalse(test_user.is_admin)
		self.assertFalse(test_user.is_staff())
		self.assertFalse(test_user.has_module_perms('core'))
		self.assertTrue(test_user.has_perm('test'))

	def test_admin_user_rights(self):
		# test admin user permissions
		test_user = User.objects.get(username="Admin")
		self.assertTrue(test_user.is_admin)
		self.assertTrue(test_user.is_staff())
		self.assertTrue(test_user.has_module_perms('core'))
		self.assertFalse(test_user.is_module_leader)
		self.assertFalse(test_user.is_office_admin)
		self.assertFalse(test_user.is_year_tutor)

	def test_user_full_rights(self):
		# test all rights work
		test_user = User.objects.get(username="Admin1")
		self.assertTrue(test_user.is_admin)
		self.assertTrue(test_user.is_staff())
		self.assertTrue(test_user.is_module_leader)
		self.assertTrue(test_user.is_office_admin)
		self.assertTrue(test_user.is_year_tutor)
		self.assertTrue(test_user.has_module_perms('core'))

	