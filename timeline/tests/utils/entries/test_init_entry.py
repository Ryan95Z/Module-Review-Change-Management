from core.models import Module, User
from core.tests.common_test_utils import ModuleTestCase
from timeline.models import TimelineEntry
from timeline.utils.entries import InitEntry


class TestInitEntry(ModuleTestCase):
    """
    Test cases for InitEntry object
    """
    def setUp(self):
        super(TestInitEntry, self).setUp()
        self.entry = InitEntry
        self.model = Module

    def test_creating_valid_entry(self):
        """
        Test case creation of a entry with a valid model.
        """
        # check the models default attributes
        init_entry = self.entry(self.model)
        self.assertEquals(init_entry.title, "{} created")
        self.assertEquals(init_entry.type, "Init")
        self.assertEquals(init_entry.model, self.model)
        self.assertEquals(init_entry.model_app_label, "core")

        # check the creation of an entry with an instance
        timeline_entry = init_entry.create(self.module)
        self.assertEquals(
            timeline_entry.title,
            init_entry.title.format(self.module.__str__())
        )

        self.assertEquals(timeline_entry.status, "Confirmed")
        self.assertEquals(timeline_entry.module_code, self.module.module_code)
        self.assertEquals(timeline_entry.object_id, self.module.pk)
        self.assertEquals(timeline_entry.entry_type, init_entry.type)

        # get the entry from the database
        db_timeline_entry = TimelineEntry.objects.get(id=timeline_entry.id)
        self.assertTrue(db_timeline_entry is not None)

    def test_assigining_entry_invalid_model(self):
        """
        Test case to enusre invalid models are not accepted
        """

        # check with None value
        with self.assertRaises(ValueError):
            self.entry(None)

        # check with a model that does not inherit the subclass
        with self.assertRaises(ValueError):
            self.entry(User)

    def test_entry_factory(self):
        """
        Test case for ensuring the factory creates
        a new instance
        """
        init_entry = self.entry(self.model)
        new_init_entry = init_entry.factory()

        # check they are difference instances
        self.assertTrue(new_init_entry != init_entry)

        # check the attributes of new instance
        self.assertEquals(new_init_entry.title, "{} created")
        self.assertEquals(new_init_entry.type, "Init")
        self.assertEquals(new_init_entry.model, self.model)
        self.assertEquals(new_init_entry.model_app_label, "core")

    def test_invalid_create_entry(self):
        """
        Test case for ensuring only valid instances
        will be processed.
        """
        init_entry = self.entry(self.model)

        with self.assertRaises(ValueError):
            init_entry.create(None)

        with self.assertRaises(ValueError):
            init_entry.create(self.module_leader)
