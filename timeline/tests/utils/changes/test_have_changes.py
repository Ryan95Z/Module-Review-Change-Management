from core.models import Module
from core.tests.common_test_utils import ModuleTestCase
from timeline.utils.changes import have_changes


class TestHaveChanges(ModuleTestCase):
    """
    Test cases for the have_changes util function
    """
    def setUp(self):
        super(TestHaveChanges, self).setUp()
        self.model = Module

    def test_have_changes_with_changes(self):
        """
        Test case for checking the desired behaviour
        """
        # provide some changes
        self.module.module_name = "A new name"
        self.module.module_credits = 65
        self.module.save()

        # check that there is some changes
        changes = have_changes(self.module.module_code, self.module)
        self.assertEquals(len(changes), 2)
        self.assertTrue('module_name' in changes)
        self.assertTrue('module_credits' in changes)

    def test_have_changs_with_no_changes(self):
        """
        Test case for ensuring that it can handle no changes
        """
        changes = have_changes(self.module.module_code, self.module)
        self.assertEquals(len(changes), 0)
        self.assertFalse(changes)

    def test_have_changes_blank_instance(self):
        """
        Test case for when either param is None
        """

        # when the instance is None
        with self.assertRaises(ValueError):
            have_changes(self.module.module_code, None)

        # when the pk is None
        with self.assertRaises(ValueError):
            have_changes(None, self.module)

    def test_have_changes_unxpected_params(self):
        """
        Test case for when the function gets params
        that don't align with the model. Should return
        an empty array.
        """

        # test with a different pk type than expected from module
        changes = have_changes(233, self.module)
        self.assertEquals(len(changes), 0)
        self.assertFalse(changes)

        # test with a model that is not used for changes
        changes = have_changes(233, self.module_leader)
        self.assertEquals(len(changes), 0)
        self.assertFalse(changes)
