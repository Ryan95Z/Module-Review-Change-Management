from django.test import Client, TestCase
from core.models import User, UserManager

"""
Util module that will contain common
test cases, templates and other parts that
are needed for test cases.
"""


class LoggedInTestCase(TestCase):
    """
    Custom base test case to test for
    views when authentication is required
    """
    def setUp(self):
        super(LoggedInTestCase, self).setUp()
        self.client = Client()
        manager = UserManager()
        manager.model = User

        # create a sample admin user
        self.admin = manager.create_superuser(
            username='admin',
            first_name='admin',
            last_name='admin',
            email='admin@example.com',
            password='password'
        )

        # create sample basic user
        self.user = manager.create_user(
            username='user1',
            first_name='user',
            last_name='user',
            email='admin@example.com',
            password='password'
        )
