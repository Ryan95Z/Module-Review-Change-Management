from django.test import TestCase
from django.db.utils import IntegrityError

from core.models import User, UserManager


class UserTestCase(TestCase):
    """
    Test case for User model
    """
    def setUp(self):
        # create a basic user
        User.objects.create(
            username="Test",
            first_name="Test",
            last_name="Last",
            email="test@example.com"
        )

        # create a admin user
        User.objects.create(
            username="Admin",
            first_name="admin",
            last_name="admin",
            email="admin@example.com",
            is_admin=True
        )

        # create a complete user with
        # all permission flags
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
        """
        Test creation of a basic user
        """
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
        """
        Test creation of an admin user
        """
        test_user = User.objects.get(username="Admin")
        self.assertTrue(test_user.is_admin)
        self.assertTrue(test_user.is_staff())
        self.assertTrue(test_user.has_module_perms('core'))
        self.assertFalse(test_user.is_module_leader)
        self.assertFalse(test_user.is_office_admin)
        self.assertFalse(test_user.is_year_tutor)

    def test_user_full_rights(self):
        """
        Test getting a user and see all access rights are correct
        """
        test_user = User.objects.get(username="Admin1")
        self.assertTrue(test_user.is_admin)
        self.assertTrue(test_user.is_staff())
        self.assertTrue(test_user.is_module_leader)
        self.assertTrue(test_user.is_office_admin)
        self.assertTrue(test_user.is_year_tutor)
        self.assertTrue(test_user.has_module_perms('core'))

    def test_user_username_already_taken(self):
        """
        Test username can only be unique when
        creating a new user.
        """
        with self.assertRaises(IntegrityError):
            User.objects.create(
                username="Test",
                first_name="Test",
                last_name="Last",
                email="test@example.com")


class UserManagerTestCase(TestCase):
    """
    Test case for UserManager object
    that is found with the user model.
    """
    def setUp(self):
        self.manager = UserManager()
        self.manager.model = User

    def test_creating_standard_user(self):
        """
        Test creation of basic user
        """
        user = self.manager.create_user(
            username='test1',
            first_name='test',
            last_name='user',
            email='test@example.com',
            password='password'
        )

        self.assertEqual(user.username, "test1")
        # make sure the manager gave all false permissions
        self.assertFalse(user.is_admin)
        self.assertFalse(user.is_staff())
        self.assertFalse(user.is_module_leader)
        self.assertFalse(user.is_office_admin)
        self.assertFalse(user.is_year_tutor)

    def test_creating_standard_user_no_username(self):
        """
        Test to determine exception is raised
        when no username is provided.
        """
        with self.assertRaises(ValueError):
            user = self.manager.create_user(
                username='',
                first_name='test',
                last_name='user',
                email='test@example.com',
                password='password'
            )

    def test_creating_standard_user_no_first_name(self):
        """
        Test to determine exception is raised
        when no first name is provided.
        """
        with self.assertRaises(ValueError):
            user = self.manager.create_user(
                username='test',
                first_name='',
                last_name='user',
                email='test@example.com',
                password='password'
            )

    def test_creating_standard_user_no_last_name(self):
        """
        Test to determine exception is raised
        when no last name is provided.
        """
        with self.assertRaises(ValueError):
            user = self.manager.create_user(
                username='test',
                first_name='test',
                last_name='',
                email='test@example.com',
                password='password'
            )

    def test_creating_standard_user_no_email(self):
        """
        Test to determine exception is raised
        when no email is provided.
        """
        with self.assertRaises(ValueError):
            user = self.manager.create_user(
                username='test',
                first_name='test',
                last_name='user',
                email='',
                password='password'
            )

    def test_creating_user_same_username(self):
        """
        Test to determine what happens when
        a user creates an account with an
        existing username.
        """

        # create the test user
        self.manager.create_user(
            username='test',
            first_name='test',
            last_name='user',
            email='test@example.com',
            password='password'
        )

        # check that the exception is raised
        with self.assertRaises(ValueError):
            user = self.manager.create_user(
                username='test',
                first_name='test',
                last_name='user',
                email='test',
                password='password'
            )

    def test_creating_super_user(self):
        """
        Test for creating a user user
        """
        user = self.manager.create_superuser(
            username='admin',
            first_name='admin',
            last_name='user',
            email='admin@example.com',
            password='password'
        )

        self.assertEqual(user.username, "admin")
        # make sure it is a superuser
        self.assertTrue(user.is_admin)
        self.assertTrue(user.is_staff())
