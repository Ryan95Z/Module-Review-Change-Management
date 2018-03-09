from django.db.models import Q
from core.models import Module
from core.tests.common_test_utils import ModuleTestCase
from timeline.utils.changes import revert_changes
from timeline.models import TimelineEntry, TableChange


class TestRevertChanges(ModuleTestCase):
    def test_revert_changes(self):
        """
        Test case for reverting valid changes from being
        pushed to the timeline.
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

        changes = TableChange.objects.filter(related_entry=recent_entry)

        # 2 changes for module_name and module_credits
        self.assertEquals(changes.count(), 2)

        completed = revert_changes(recent_entry.pk)
        self.assertTrue(completed)

        # check the model has its original values
        module = Module.objects.get(pk=self.module.pk)
        self.assertEquals(module.module_name, name)
        self.assertEquals(module.module_credits, credits)

        # check there is not changes
        changes = TableChange.objects.filter(related_entry=recent_entry)
        self.assertEquals(changes.count(), 0)

    def test_valid_revert_changes_with_no_changes(self):
        """
        Test case for testing that it can work if entry
        that has not changes is passed
        """
        entry = TimelineEntry.objects.filter(status="Confirmed")[0]
        completed = revert_changes(entry.pk)
        self.assertFalse(completed)

    def test_invalid_entry_pk_revert_changes(self):
        """
        Test case for check exception is raised if
        invalid entry pk is provided
        """
        # with None value
        with self.assertRaises(ValueError):
            revert_changes(None)

        # with zero value
        with self.assertRaises(ValueError):
            revert_changes(0)

        # with extreme negative number
        with self.assertRaises(ValueError):
            revert_changes(-12440)

