from django.test import TestCase
from core.models import User


class BasicUserTestCase(TestCase):
    """
    Base test case that contains sample users
    """
    def setUp(self):
        super(BasicUserTestCase, self).setUp()
        self.user1 = User.objects.create(
            username="user1",
            first_name="user",
            last_name="user",
            email="user@example.com",
        )

        self.user2 = User.objects.create(
            username="user2",
            first_name="user2",
            last_name="use2",
            email="user2@example.com",
        )

        self.admin = User.objects.create(
            username="admin",
            first_name="admin",
            last_name="admin",
            email="admin@example.com",
            is_admin=True
        )
