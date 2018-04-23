from core.tests.common_test_utils import ModuleTestCase
from timeline.tests.common import BasicUserTestCase
from timeline.utils.timeline.factory import EntryFactory
from timeline.utils.timeline.entries import InitEntry, UpdateEntry


class TestEntryFactroy(BasicUserTestCase, ModuleTestCase):
    """
    Test case for the EntryFactory for timeline
    """
    def setUp(self):
        super(TestEntryFactroy, self).setUp()
        self.factory = EntryFactory

    def test_valid_factory_state(self):
        """
        Test case for checking the state of the factory is valid
        """
        factories = self.factory.factories

        # check the objects are present
        self.assertEquals(factories["Init"], InitEntry)
        self.assertEquals(factories["Update"], UpdateEntry)

        instances = self.factory.assigned_instances()
        self.assertEquals(len(instances), 3)

    def test_valid_factory_get(self):
        """
        Test getting valid object from factory
        """
        alias = ["Init", "Update"]
        objs = [InitEntry, UpdateEntry]

        for index, k in enumerate(alias):
            result = self.factory.get(k)
            self.assertEquals(result, objs[index])

    def test_factory_get_invalid_params(self):
        """
        Test for ensuring get in factory can handle errors
        """
        # test exception is raises
        invalid_alias = [None, ""]
        for alias in invalid_alias:
            with self.assertRaises(ValueError):
                self.factory.get(alias)

        # test none is returned with invalid name
        result = self.factory.get("Hello")
        self.assertEquals(result, None)

    def test_factory_makeEntry(self):
        """
        Test entries can be created from factory
        """
        alias = ["Init", "Update"]
        objs = [InitEntry, UpdateEntry]

        # check each object is created as expected
        for index, k in enumerate(alias):
            result = self.factory.makeEntry(k, self.module)
            self.assertEquals(result, objs[index](self.module))

    def test_factory_makeEntry_invlaid_params(self):
        """
        Test makeEntry method to ensure it can handle invalid parameters
        """
        # test invalid alias
        invalid_alias = [None, ""]
        for alias in invalid_alias:
            with self.assertRaises(ValueError):
                self.factory.makeEntry(alias, self.module)

        # test invalid model
        with self.assertRaises(ValueError):
            self.factory.makeEntry("Init", None)
