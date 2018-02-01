from django.db import IntegrityError
from django.test import TestCase
from core.models import (Reviewer, ReviewerManager, User, UserManager)

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
            username="johndoe",
            first_name="John",
            last_name="Doe",
            email="doe@test.com",
            password="password"
        )

    def test_create_new_model_instance(self):
        """
        Ensure that the manager can correctly create
        a new user model and include it in the reviewer model.
        """
        module_code = "CM1101"
        username = "johndoe"
        first_name = "John"
        last_name = "Doe"
        email = "doe@test.com"
        password = "password"

        # create the model
        model = self.manager.create_new_tutor(
            module_code=module_code,
            username=username,
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=password
        )

        self.assertEquals(model.module_code, module_code)
        self.assertEquals(model.get_reviewer_name(), "{} {}".format(first_name, last_name))
        self.assertEquals(model.get_reviewer_username(), username)

        user = model.reviewer_user
        self.assertEquals(user.email, email)
        # check that manager set the permission to be true
        self.assertTrue(user.is_reviewer)

    def test_create_model_existing_user(self):
        """
        Creating a module reviewer from an existing user.
        """
        module_code = "CM1101"

        # check permission is not already set
        self.assertFalse(self.user.is_reviewer)

        model = self.manager.create_reviewer(module_code, self.user)

        self.assertEquals(model.module_code, module_code)
        self.assertEquals(model.get_reviewer_name(), self.user.get_full_name())
        self.assertEquals(model.get_reviewer_username(), self.user.username)

        # check that the permissions were updated
        user = model.reviewer_user
        self.assertEquals(user.email, self.user.email)
        self.assertTrue(self.user.is_reviewer)

    def test_create_reviewer_with_no_user(self):
        """
        Test case for checking that a reviewer cannot be
        created if there is no user provided.
        """
        module_code = "CM1101"
        with self.assertRaises(ValueError):
            self.manager.create_tutor(module_code, None)

    def test_create_reviewer_with_no_module_code(self):
        """
        Test case for checking that an invaid string
        for tutor year will not create a model.
        """
        with self.assertRaises(ValueError):
            self.manager.create_tutor("", self.user)

class ReviewerTests(TestCase):
    """
    Test cases for Reviewer
    """
    def setUp(self):
        super(ReviewerManagerTests, self).setUp()
        self.model = Reviewer

        user_manager = UserManager()
        user_manager.model = User

        self.user = user_manager.create_user(
            username="johndoe",
            first_name="John",
            last_name="Doe",
            email="doe@test.com",
            password="password"
        )

    def test_valid_reviewer(self):
        """
        Test case to check that the model
        is valid with expected data.
        """
        self.model.objects.create(
            module_code="CM1101",
            reviewer_user=self.user
        )

        reviewer = Reviewer.objects.get(pk=1)

        self.assertEquals(tutor.module_code, "CM1101")
        self.assertEquals(tutor.get_reviewer_name(), self.user.get_full_name())
        self.assertEquals(tutor.get_reviewer_username(), self.user.username)
        self.assertEquals(tutor.get_reviewer_id(), self.user.id)

