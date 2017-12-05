from django.test import TestCase
from core.forms import LoginForm

class LoginFormTest(TestCase):
	def setUp(self):
		super(LoginFormTest, self).setUp()

	def test_valid_login_form(self):
		form = LoginForm({
			'username' : 'admin',
			'password' : 'password'
		})

		self.assertTrue(form.is_valid())
		self.assertEquals(form.cleaned_data['username'], 'admin')
		self.assertEquals(form.cleaned_data['password'], 'password')

	def test_invalid_login_form(self):
		form = LoginForm({})
		self.assertFalse(form.is_valid())
		self.assertEqual(form.errors['username'], ['This field is required.'])