from core.models import Module
from core.tests.common_test_utils import LoggedInTestCase
from timeline.utils.timeline.helpers import publish_changes
from timeline.models import TimelineEntry


class TestPublishChanges(LoggedInTestCase):
    """
    Test case for the helper function publish_changes
    """
    def setUp(self):
        super(TestPublishChanges, self).setUp()
        self.model = TimelineEntry
        self.function = publish_changes

    def test_valid_publish_changes(self):
        """
        Test case for creating a timeline entry when a model is provided
        """
        module = Module.objects.create(
            module_code="CM3301",
            module_name="Test Module",
            module_credits="10",
            module_level="L1",
            semester="Autumn Semester",
            delivery_language="English",
            module_leader=self.user
        )

        entry = self.function(module, self.user)

        # check the model created
        self.assertTrue(isinstance(entry, self.model))
        self.assertEquals(entry.status, "Confirmed")
        self.assertEquals(entry.content_object, module)
        self.assertEquals(entry.module_code, module.module_code)

        # check it is in the database
        entry_db = self.model.objects.get(pk=entry.pk)
        self.assertEquals(entry_db, entry)

        # check it is the first in the timeline
        module_entries = self.model.objects.filter(
            module_code=module.module_code
        )
        self.assertEquals(module_entries.count(), 1)
