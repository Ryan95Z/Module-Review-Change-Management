from django.db import IntegrityError
from django.test import TestCase
from core.models import (Reviewer, ReviewerManager, User, UserManager, Module)


class ReviewerManagerTests(TestCase):
    """
    Test cases for ReviewerManager
    """
    def setUp(self):
        super(ReviewerManagerTests, self).setUp()
        self.manager = ReviewerManager()
        self.manager.model = Reviewer

        # create a test user
        user_manager = UserManager()
        user_manager.model = User
        self.user = user_manager.create_user(
            username="test",
            first_name="test",
            last_name="test",
            email="test@test.com",
            password="password"
        )

        # create another test user to be used a module leader
        # (module leader model not implemented atm)
        self.module_leader = user_manager.create_user(
            username="leader",
            first_name="Module",
            last_name="Leader",
            email="ml@test.com",
            password="password"
        )

        # create a test module
        module_model = Module
        self.module = module_model.objects.create(
            module_code="CM1101",
            module_name="Test Module",
            module_credits="10",
            module_level="1",
            module_year="1",
            semester="Autumn Semester",
            delivery_language="English",
            module_leader=self.module_leader
        )

    def test_create_new_model_instance(self):
        """
        Ensure that the manager can correctly create
        a new user model and include it in the reviewer model.
        """
        module = self.module
        username = "johndoe"
        first_name = "John"
        last_name = "Doe"
        email = "doe@test.com"
        password = "password"

        # create the model
        model = self.manager.create_new_reviewer(
            modules=[module],
            username=username,
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=password
        )

        self.assertEquals(model.modules.get(module_code="CM1101"), module)
        self.assertEquals(model.get_reviewer_name(), "{} {}".format(first_name, last_name))
        self.assertEquals(model.get_reviewer_username(), username)

        user = model.user
        self.assertEquals(user.email, email)
        # check that manager set the permission to be true
        self.assertTrue(user.is_module_reviewer)

    def test_create_model_existing_user(self):
        """
        Creating a module reviewer from an existing user.
        """
        module = self.module

        # check permission is not already set
        self.assertFalse(self.user.is_module_reviewer)

        model = self.manager.create_reviewer([module], self.user)

        self.assertEquals(model.modules.get(module_code="CM1101"), module)
        self.assertEquals(model.get_reviewer_name(), self.user.get_full_name())
        self.assertEquals(model.get_reviewer_username(), self.user.username)

        # check that the permissions were updated
        user = model.user
        self.assertEquals(user.email, self.user.email)
        self.assertTrue(self.user.is_module_reviewer)

    def test_create_reviewer_with_no_user(self):
        """
        Check that a model will not be created without a user
        """
        module = self.module
        with self.assertRaises(ValueError):
            self.manager.create_reviewer([module], None)

    def test_create_reviewer_with_no_module(self):
        """
        Check that a model will not be created without a module
        """
        with self.assertRaises(ValueError):
            self.manager.create_reviewer(None, self.user)


class ReviewerTests(TestCase):
    """
    Test cases for Reviewer
    """
    def setUp(self):
        super(ReviewerTests, self).setUp()
        self.model = Reviewer

        user_manager = UserManager()
        user_manager.model = User

        # create a test user
        self.user = user_manager.create_user(
            username="johndoe",
            first_name="John",
            last_name="Doe",
            email="doe@test.com",
            password="password"
        )

        # create another test user to be used a module leader
        # (module leader model not implemented atm)
        self.module_leader = user_manager.create_user(
            username="leader",
            first_name="Module",
            last_name="Leader",
            email="ml@test.com",
            password="password"
        )

        # create a test module
        module_model = Module
        self.module = module_model.objects.create(
            module_code="CM1101",
            module_name="Test Module",
            module_credits="10",
            module_level="1",
            module_year="1",
            semester="Autumn Semester",
            delivery_language="English",
            module_leader=self.module_leader
        )

    def test_valid_reviewer(self):
        """
        Test case to check that the model
        is valid with expected data.
        """
        reviewer = self.model.objects.create(
            user=self.user
        )
        reviewer.modules.add(self.module)
        reviewer.save()

        self.assertEqual(reviewer.modules.get(module_code="CM1101"), self.module)
        self.assertEquals(reviewer.get_reviewer_name(), self.user.get_full_name())
        self.assertEquals(reviewer.get_reviewer_username(), self.user.username)
        self.assertEquals(reviewer.get_reviewer_id(), self.user.id)

    def test_reviewer_cascade_deleted_user(self):
        """
        If the user is deleted, the reviewer should
        also be deleted.
        """

        # First create the reviewer and ensure that it was actually created
        reviewer = self.model.objects.create(
            user=self.user
        )
        reviewer.modules.add(self.module)
        reviewer.save()
        reviewer_id = reviewer.id

        self.assertEqual(reviewer.modules.get(module_code="CM1101"), self.module)

        # Then delete the user and check if the reviewer was also deleted
        self.user.delete()

        with self.assertRaises(User.DoesNotExist):
            User.objects.get(username="johndoe")

        with self.assertRaises(Reviewer.DoesNotExist):
            Reviewer.objects.get(id=reviewer_id)

    def test_reviewer_cascade_deleted_module(self):
        """
        If a module is deleted, the reviewer should remain, but the said
        module should not be associated.
        """

        # First create the reviewer and ensure that it was actually created
        reviewer = self.model.objects.create(
            user=self.user
        )
        reviewer.modules.add(self.module)
        reviewer.save()
        reviewer_id = reviewer.id
        self.assertEqual(reviewer.modules.get(module_code="CM1101"), self.module)
        self.module.delete()

        self.assertEquals(reviewer.get_reviewer_name(), self.user.get_full_name())
        with self.assertRaises(Module.DoesNotExist):
            reviewer.modules.get(module_code="CM1101")

        # make sure the reviewer created in test is deleted
        with self.assertRaises(self.model.DoesNotExist):
            self.model.objects.get(id=reviewer_id)
