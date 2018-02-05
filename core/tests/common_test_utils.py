from importlib import import_module
from django.test import Client, TestCase
from django.conf import settings
from core.models import User, UserManager, Module
from abc import ABC, abstractmethod

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
        # set up sessions in unit tests
        session_engine = import_module(settings.SESSION_ENGINE)
        store = session_engine.SessionStore()
        store.save()
        # set the client
        self.client = Client()
        self.client.cookies[settings.SESSION_COOKIE_NAME] = store.session_key
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

class ModuleTestCase(TestCase):
    """
    Custom base test case which can be used
    to test views which require modules
    """
    def setUp(self):
        super(ModuleTestCase, self).setUp()

        manager = UserManager()
        manager.model = User
        
        # Create a sample module leader
        self.module_leader = manager.create_user(
            username='moduleleader',
            first_name='Module',
            last_name='Leader',
            email='ml@example.com',
            password='password'
        )

        # Create a test module
        self.module = Module.objects.create(
            module_code = "CMXXXX",
            module_name = "Test Module",
            module_credits = "10",
            module_level = "L1",
            module_year = "Year 1",
            semester = "Autumn Semester",
            delivery_language = "English",
            module_leader = self.module_leader
        )


class BaseViewTestCase(LoggedInTestCase, ABC):
    """
    Abstract class that provides a standard template that
    will need to be inherited by any base class for executing views.
    Provides 5 basic methods that are essential for testing any view.
    """

    @abstractmethod
    def run_get_view(self, url):
        """
        Executes view tests to get the view.
        Expected return: Response from calling the view
        """
        pass

    @abstractmethod
    def run_get_view_incorrect_access(self, url):
        """
        Executes view tests to check users with
        incorrect access cannot see the view.
        Expected return: Response from calling the view
        """
        pass

    @abstractmethod
    def run_get_view_not_logged_in(self, url):
        """
        Executes view tests to check it cannot
        be accessed unless logged in.
        Expected return: Response from calling the view
        """
        pass

    @abstractmethod
    def run_valid_post_view(self, url, data):
        """
        Executes view tests for a valid post request.
        Expected return: Response from calling the view
        """
        pass

    @abstractmethod
    def run_invalid_post_view(self, url, data):
        """
        Executes view tests for an invalid post request.
        Expected return: Response from calling the view
        """
        pass
