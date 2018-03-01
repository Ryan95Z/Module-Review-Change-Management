from django.db.models import Q
from core.models import Module
from core.tests.common_test_utils import ModuleTestCase
from timeline.utils.changes import process_changes
from timeline.models import TimelineEntry


class TestProcessChanges(ModuleTestCase):
    """
    Test case for the utility function process_changes
    """

    def test_process_changes(self):
        """
        Test case fpr processing valid data for a model
        """
        name = self.module.module_name
        credits = int(self.module.module_credits)

        new_name = "New Module Name"
        new_credits = 56

        # make changes to the module so it will populate table change table
        self.module.module_name = new_name
        self.module.module_credits = new_credits
        self.module.save()

        # check that the changes have not been made to the database
        module = Module.objects.get(pk=self.module.pk)
        self.assertEquals(module.module_name, name)
        self.assertEquals(module.module_credits, credits)

        # get the entry
        recent_entry = TimelineEntry.objects.filter(
            Q(changes__icontains=new_name))[0]

        # process changes
        completed = process_changes(recent_entry.pk)
        self.assertTrue(completed)

        # check that the changes were process
        module = Module.objects.get(pk=self.module.pk)
        self.assertEquals(module.module_name, new_name)
        self.assertEquals(module.module_credits, new_credits)

    def test_invalid_pk_process_changes(self):
        """
        Test case for checking that invalid pks are not processed
        """
        with self.assertRaises(ValueError):
            process_changes(-1000)

        with self.assertRaises(ValueError):
            process_changes(0)

        with self.assertRaises(ValueError):
            process_changes(None)

    def test_valid_pk_no_changes(self):
        """
        Test case for a valid pk with no changes to process.
        """

        completed = process_changes(100)
        self.assertTrue(completed)
