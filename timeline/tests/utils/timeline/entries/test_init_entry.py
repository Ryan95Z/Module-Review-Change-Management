from core.models import Module
from core.tests.common_test_utils import LoggedInTestCase
from timeline.models import TimelineEntry
from timeline.utils.timeline.entries import InitEntry, INIT


class TestInitEntry(LoggedInTestCase):
    """
    Test case for InitEntry object
    """
    def setUp(self):
        super(TestInitEntry, self).setUp()
        self.entry = InitEntry
        self.module_data = {
            "module_code": "CM3301",
            "module_name": "Test Module",
            "module_credits": "10",
            "module_level": "L1",
            "semester": "Autumn Semester",
            "delivery_language": "English",
            "module_leader": self.user
        }
        self.module = Module.objects.create(**self.module_data)
        self.model = TimelineEntry

    def test_valid_entry_creation(self):
        """
        Test the creation of a init entry
        """
        entry = self.entry(self.module)

        sum_changes = "{} has been created for {}".format(
            self.module.title(),
            self.module.module_code
        )

        self.assertEquals(entry.model, self.module)
        self.assertEquals(entry.entry_varient, INIT)
        self.assertEquals(entry.changes, None)

        self.assertEquals(entry.get_module_code(), self.module.module_code)
        self.assertEquals(entry.title(), self.module.title())
        self.assertEquals(entry.type_of_entry(), INIT)
        self.assertEquals(entry.model_class_object(), Module)
        self.assertTrue(entry.have_changes())

        # no markdown as there are no changes
        self.assertEquals(entry.content(), '')

        self.assertEquals(entry.sum_changes(), sum_changes)
