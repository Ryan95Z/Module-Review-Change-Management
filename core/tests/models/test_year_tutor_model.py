from django.db import IntegrityError
from django.test import TestCase
from core.models import (YearTutor, YearTutorManager, User, UserManager)


class YearTutorManagerTests(TestCase):
    """
    Test cases for YearTutorManager
    """
    def setUp(self):
        super(YearTutorManagerTests, self).setUp()
        self.manager = YearTutorManager()
        self.manager.model = YearTutor

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

    def test_create_new_model_instance(self):
        """
        Test case to ensure that manager can correctly create
        a new user model and include it into year tutor.
        """
        tutor_year = "year 1"
        username = "Test"
        first_name = "test"
        last_name = "test"
        email = "test@test.com"
        password = "password"

        # create the model
        model = self.manager.create_new_tutor(
            tutor_year=tutor_year,
            username=username,
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=password
        )

        self.assertEquals(model.tutor_year, tutor_year)
        self.assertEquals(model.get_tutor_name(), "{} {}".format(
            first_name, last_name))
        self.assertEquals(model.get_tutor_username(), username)

        user = model.year_tutor_user
        self.assertEquals(user.email, email)
        # check that manager set the permission to be true
        self.assertTrue(user.is_year_tutor)

    def test_create_model_existing_user(self):
        """
        Test case for creating a year tutor from an existing
        user model.
        """
        tutor_year = "Year 1"

        # check permission is not already set
        # for being a year tutor
        self.assertFalse(self.user.is_year_tutor)

        model = self.manager.create_tutor(tutor_year, self.user)

        self.assertEquals(model.tutor_year, tutor_year)
        self.assertEquals(model.get_tutor_name(), self.user.get_full_name())
        self.assertEquals(model.get_tutor_username(), self.user.username)

        # check that the permissions were updated
        user = model.year_tutor_user
        self.assertEquals(user.email, self.user.email)
        self.assertTrue(self.user.is_year_tutor)

    def test_create_tutor_with_no_user(self):
        """
        Test case for checking that a model is not
        created if there is no user provded.
        """
        tutor_year = "year 1"
        with self.assertRaises(ValueError):
            self.manager.create_tutor(tutor_year, None)

    def test_create_tutor_with_no_tutor_year(self):
        """
        Test case for checking that an invaid string
        for tutor year will not create a model.
        """
        with self.assertRaises(ValueError):
            self.manager.create_tutor("", self.user)

    def test_create_tutor_one_to_one_violation(self):
        """
        Test to check that the one to one relationship
        will not create a model is violated.
        """
        tutor_year = "Year 1"
        self.manager.create_tutor(tutor_year, self.user)

        tutor = self.manager.create_tutor(tutor_year, self.user)
        self.assertEquals(tutor, None)


class YearTutorTests(TestCase):
    """
    Test cases for YearTutor
    """
    def setUp(self):
        super(YearTutorTests, self).setUp()
        self.model = YearTutor

        user_manager = UserManager()
        user_manager.model = User

        self.user = user_manager.create_user(
            username="test",
            first_name="test",
            last_name="test",
            email="test@test.com",
            password="password"
        )

    def test_valid_year_tutor(self):
        """
        Test case to check that the model
        is valid with expected data.
        """
        self.model.objects.create(
            tutor_year="Year 1",
            year_tutor_user=self.user
        )

        # test getting the model
        tutor = YearTutor.objects.get(pk=1)

        self.assertEquals(tutor.tutor_year, "Year 1")
        self.assertEquals(tutor.get_tutor_name(), self.user.get_full_name())
        self.assertEquals(tutor.get_tutor_username(), self.user.username)
        self.assertEquals(tutor.get_tutor_id(), self.user.id)

    def test_year_tutor_one_to_one_error(self):
        """
        Test case to see that one to one is maintained
        if user that is already assigned to a model
        is assigned again.
        """

        # create a valid object first
        self.model.objects.create(
            tutor_year="Year 1",
            year_tutor_user=self.user
        )

        # create a second one that tries to assign
        # a user that is already linked one to one
        with self.assertRaises(IntegrityError):
            self.model.objects.create(
                tutor_year="Year 1",
                year_tutor_user=self.user
            )

    def test_year_tutor_with_random_tutor_string(self):
        """
        Test case to see that model could handle
        a different year that is not in the choices
        that is currently defined in the model.
        """

        # this should not matter since chocies
        # are mainly used on the GUI. Though should
        # still be able to handle this.
        string = "Year 5"
        tutor = self.model.objects.create(
            tutor_year=string,
            year_tutor_user=self.user
        )

        self.assertEquals(tutor.tutor_year, string)
        self.assertEquals(tutor.get_tutor_name(), self.user.get_full_name())
        self.assertEquals(tutor.get_tutor_username(), self.user.username)
        self.assertEquals(tutor.get_tutor_id(), self.user.id)
