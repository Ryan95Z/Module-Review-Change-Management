from core.models import Module
from core.tests.common_test_utils import LoggedInTestCase, ModuleTestCase
from timeline.models import TimelineEntry
from timeline.utils.timeline.entries import UpdateEntry, UPDATE


class TestUpdateEntry(LoggedInTestCase, ModuleTestCase):
    """
    Test case for UpdateEntry object
    """
    def setUp(self):
        super(TestUpdateEntry, self).setUp()

        # previous data from module
        self.old_module_name = self.module.module_name
        self.old_credits = self.module.module_credits

        # new data for module
        self.new_module_name = "Hello World"
        self.new_credits = "42"

        # update the module to trigger the differences
        self.module.module_name = self.new_module_name
        self.module.module_credits = self.new_credits

        self.entry = UpdateEntry
        self.model = TimelineEntry

    def test_valid_entry_creation_with_changes(self):
        """
        Test the creation of a entry when there are changes.
        """
        expected_diff = {
            'module_name': (self.old_module_name, self.new_module_name),
            'module_credits': (self.old_credits, self.new_credits)
        }

        expected_content = "* module name: {} -> {}\n".format(
            self.old_module_name,
            self.new_module_name
        )

        expected_content += "* module credits: {} -> {}\n".format(
            self.old_credits,
            self.new_credits
        )

        expected_sum_changes = "There are 2 changes to {}".format(
            self.module.title()
        )

        entry = UpdateEntry(self.module)
        self.assertEquals(entry.model, self.module)
        self.assertEquals(entry.entry_varient, UPDATE)

        # check the data for the entry
        self.assertEquals(entry.get_module_code(), self.module.module_code)
        self.assertEquals(entry.title(), self.module.title())
        self.assertEquals(entry.type_of_entry(), UPDATE)
        self.assertEquals(entry.model_class_object(), Module)
        self.assertTrue(entry.have_changes())

        # Test the generated content
        # since the content can be generated in different orders
        # we count the length of the string, which should be equal
        self.assertEquals(len(entry.content()), len(expected_content))
        self.assertEquals(entry.sum_changes(), expected_sum_changes)

        # assert that the differences are the same
        self.assertEquals(entry.get_differences(), expected_diff)

        # create and test the timeline entry
        timeline_entry = entry.create_entry()
        self.assertEquals(timeline_entry.title, self.module.title())
        self.assertEquals(len(timeline_entry.changes), len(expected_content))
        self.assertEquals(timeline_entry.content_object, self.module)
        self.assertEquals(timeline_entry.status, "Draft")
        self.assertEquals(timeline_entry.changes_by, None)

    def test_valid_entry_no_changes(self):
        """
        Test that an entry is not created if there are no changes
        to a model.
        """
        expected_sum_changes = "There are 0 changes to {}".format(
            self.module_two.title()
        )

        entry = UpdateEntry(self.module_two)
        self.assertEquals(entry.model, self.module_two)
        self.assertEquals(entry.entry_varient, UPDATE)

        # test the general data of the entry
        self.assertEquals(entry.get_module_code(), self.module_two.module_code)
        self.assertEquals(entry.title(), self.module_two.title())
        self.assertEquals(entry.type_of_entry(), UPDATE)
        self.assertEquals(entry.model_class_object(), Module)
        self.assertFalse(entry.have_changes())

        # test the generated content
        self.assertEquals(entry.sum_changes(), expected_sum_changes)
        self.assertEquals(entry.content(), '')

        # assert that entry is not created if no changes
        timeline_entry = entry.create_entry()
        self.assertEquals(timeline_entry, None)
