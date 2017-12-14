from django.db import IntegrityError
from django.test import TestCase
from core.models import YearTutor, User, UserManager


class YearTutorTests(TestCase):
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
