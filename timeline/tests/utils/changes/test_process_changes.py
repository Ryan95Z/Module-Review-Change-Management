from django.db.models import Q

from core.models import Module, User
from core.tests.common_test_utils import ModuleTestCase

from timeline.models import TimelineEntry
from timeline.utils.changes import process_changes
from timeline.utils.notifications.helpers import WatcherWrapper


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
        # extreme negative numbers
        with self.assertRaises(ValueError):
            process_changes(-1000)

        # zero value
        with self.assertRaises(ValueError):
            process_changes(0)

        # None
        with self.assertRaises(ValueError):
            process_changes(None)

    def test_valid_pk_no_changes(self):
        """
        Test case for a valid pk with no changes to process.
        """
        completed = process_changes(100)
        self.assertTrue(completed)

    def test_changing_module_leader_watcher(self):
        """
        Test case for ensuring that watchers are updated
        for a module leader when that change is made. Also
        provides a test for the foreign key changes that need
        to be processed.
        """
        new_module_leader = User.objects.create_user(
            username='ml1',
            first_name='bill',
            last_name='test',
            email='bill@test.com',
            password='billwashere'
        )

        # add the current module leader to a watcher object
        current_module_leader_watch = WatcherWrapper(self.module_leader)
        current_module_leader_watch.add_module(self.module)
        n_modules_watched = current_module_leader_watch.modules().count()

        # check that the module has been added
        self.assertEquals(n_modules_watched, 1)

        # make changes to module leader
        self.module.module_leader = new_module_leader
        self.module.save()

        # check that module leader has not changed
        module = Module.objects.get(pk=self.module.pk)
        self.assertEquals(module.module_leader, self.module_leader)

        # get the entry
        recent_entry = TimelineEntry.objects.filter(
            Q(changes__icontains=new_module_leader.username))[0]

        # process changes
        completed = process_changes(recent_entry.pk)
        self.assertTrue(completed)

        # check that the module leader has been changed
        module = Module.objects.get(pk=self.module.pk)
        self.assertEquals(module.module_leader, new_module_leader)

        # check the watchers have been swapped
        # check the original module leader is 0
        n_modules_watched = current_module_leader_watch.modules().count()
        self.assertEquals(n_modules_watched, 0)

        # check the new module leader
        new_module_leader_watch = WatcherWrapper(new_module_leader)
        n_modules_watched = new_module_leader_watch.modules().count()
        self.assertEquals(n_modules_watched, 1)
