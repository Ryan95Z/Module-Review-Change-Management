from django.test import TestCase
from django.db.utils import IntegrityError
from django.core.exceptions import ValidationError
from core.models import Module, ModuleManager, UserManager, User


class TestModuleManager(TestCase):
    """
    Unit test for ModuleManager
    """
    def setUp(self):
        super(TestModuleManager, self).setUp()
        self.manager = ModuleManager()
        self.manager.model = Module

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
        Test case for creating a model from the manager
        """
        code = "CM3301"
        name = "Software Engineering Project"
        credits = 40
        level = "l3"
        semester = "Double Semester"
        lang = "English"

        # check that the user is not a module leader
        self.assertFalse(self.user.is_module_leader)

        model = self.manager.create_module(
            module_code=code,
            module_name=name,
            module_credits=credits,
            module_level=level,
            semester=semester,
            delivery_language=lang,
            module_leader=self.user
        )

        # check that the user's permission's has been updated
        self.assertTrue(self.user.is_module_leader)

        # check that the model was created
        self.assertEquals(model.module_code, code)
        self.assertEquals(model.module_name, name)
        self.assertEquals(model.module_credits, credits)
        self.assertEquals(model.module_level, level)
        self.assertEquals(model.semester, semester)
        self.assertEquals(model.delivery_language, lang)
        self.assertEquals(model.module_leader, self.user)

    def test_create_new_model_no_module_leader(self):
        """
        Test case for manager when no module leader is provided
        """
        code = "CM3301"
        name = "Software Engineering Project"
        credits = 40
        level = "l3"
        semester = "Double Semester"
        lang = "English"

        # check that an exception is thrown
        # if module leader is None
        with self.assertRaises(IntegrityError):
            self.manager.create_module(
                module_code=code,
                module_name=name,
                module_credits=credits,
                module_level=level,
                semester=semester,
                delivery_language=lang,
                module_leader=None
            )

    def test_create_new_model_invalid_credit_range(self):
        """
        Test case to assert credits cannot be greater
        than or below specific ranges.
        """

        # inital values
        code = "CM3301"
        name = "Software Engineering Project"
        level = "l3"
        semester = "Double Semester"
        lang = "English"

        # array of credi types
        credits = [400, 0, -340, 9, 2]

        # loop through each one to ensure that
        # an exception will occur
        for credit in credits:
            with self.assertRaises(ValueError):
                self.manager.create_module(
                    module_code=code,
                    module_name=name,
                    module_credits=credit,
                    module_level=level,
                    semester=semester,
                    delivery_language=lang,
                    module_leader=self.user
                )


class TestModule(TestCase):
    def setUp(self):
        super(TestModule, self).setUp()
        user_manager = UserManager()
        user_manager.model = User

        self.model = Module
        self.user = user_manager.create_user(
            username="test",
            first_name="test",
            last_name="test",
            email="test@test.com",
            password="password"
        )

    def test_create_valid_model(self):
        """
        Test case for creation of a valid module
        """
        code = "CM3301"
        name = "Software Engineering Project"
        credits = 40
        level = "l3"
        semester = "Double Semester"
        lang = "English"

        module = self.model.objects.create(
            module_code=code,
            module_name=name,
            module_credits=credits,
            module_level=level,
            semester=semester,
            delivery_language=lang,
            module_leader=self.user
        )

        # check that the model was created
        self.assertEquals(module.module_code, code)
        self.assertEquals(module.module_name, name)
        self.assertEquals(module.module_credits, credits)
        self.assertEquals(module.module_level, level)
        self.assertEquals(module.semester, semester)
        self.assertEquals(module.delivery_language, lang)
        self.assertEquals(module.module_leader, self.user)

        # test model methods
        self.assertEquals(
            module.module_leader_name(),
            self.user.get_full_name()
        )

        self.assertEquals(module.module_leader_username(), self.user.username)
        self.assertEquals(module.module_leader_id, self.user.id)

    def test_create_model_with_invalid_credits_range(self):
        """
        Test case for asserting validators work
        """
        # base values for testing
        code = "CM3301"
        name = "Software Engineering Project"
        level = "l3"
        semester = "Double Semester"
        lang = "English"

        #  assert for negative credits
        credits = -4000

        with self.assertRaises(ValidationError):
            # validators on occur when full clean is
            # applied on the model. It does not check
            # during the create method
            model = self.model.objects.create(
                module_code=code,
                module_name=name,
                module_credits=credits,
                module_level=level,
                semester=semester,
                delivery_language=lang,
                module_leader=self.user
            ).full_clean()

        # remove model for next assert
        self.model.objects.get(module_code=code).delete()

        # assert zero credits
        credits = 0
        with self.assertRaises(ValidationError):
            model = self.model.objects.create(
                module_code=code,
                module_name=name,
                module_credits=credits,
                semester=semester,
                delivery_language=lang,
                module_leader=self.user
            ).full_clean()
        # remove model for next assert
        self.model.objects.get(module_code=code).delete()

        # asert for large positive credits
        credits = 10000
        with self.assertRaises(ValidationError):
            model = self.model.objects.create(
                module_code=code,
                module_name=name,
                module_credits=credits,
                semester=semester,
                delivery_language=lang,
                module_leader=self.user
            ).full_clean()

    def test_module_code_is_unique(self):
        """
        Test case to ensure that no two modules
        can have the same module code.
        """
        code = "CM3301"
        name = "Software Engineering Project"
        credits = 40
        level = "l3"
        semester = "Double Semester"
        lang = "English"

        # create initial model
        self.model.objects.create(
            module_code=code,
            module_name=name,
            module_credits=credits,
            semester=semester,
            delivery_language=lang,
            module_leader=self.user
        )

        name = "Applied Software Engineering Project"

        # create model again to check it is not possible
        with self.assertRaises(IntegrityError):
            self.model.objects.create(
                module_code=code,
                module_name=name,
                module_credits=credits,
                semester=semester,
                delivery_language=lang,
                module_leader=self.user
            )
