from django.test import TestCase
from core.models import User, Module


class BaseTimelineModelTestCase(TestCase):
        def setUp(self):
            # create a test user
            self.user = User.objects.create_user(
                username="test",
                first_name="test",
                last_name="test",
                email="test@test.com",
                password="password"
            )

            # create a test module
            self.module = Module.objects.create_module(
                module_code="CM1234",
                module_name="Software Engineering",
                module_credits=40,
                module_level="L6",
                semester="Double Semester",
                delivery_language="English",
                module_leader=self.user
            )
