from django.test import TestCase
from django.db.utils import IntegrityError
from core.models import User, Module
from timeline.models import TimelineEntry


class TestTimelineEntry(TestCase):
    """
    Test case for the TimelineEntry model
    """
    def setUp(self):
        super(TestTimelineEntry, self).setUp()
        self.model = TimelineEntry

        # create a test user
        self.user = User.objects.create_user(
            username="test",
            first_name="test",
            last_name="test",
            email="test@test.com",
            password="password"
        )

        # create a test module
        self.module = Module.objects.create_module(
            module_code="CM1234",
            module_name="Software Engineering",
            module_credits=40,
            module_level="L6",
            semester="Double Semester",
            delivery_language="English",
            module_leader=self.user
        )

    def test_create_valid_model(self):
        """
        Unit test for creating a valid model
        """
        title = "Test Changes"
        changes = "Test changes to report"
        status = "Draft",
        entry_type = "Generic"
        module = self.module

        entry = TimelineEntry.objects.create(
            title=title,
            changes=changes,
            status=status,
            entry_type=entry_type,
            module=module,
            approved_by=self.user
        )

        # check the attributes
        self.assertEquals(entry.title, title)
        self.assertEquals(entry.changes, changes)
        self.assertEquals(entry.status, status)
        self.assertEquals(entry.entry_type, entry_type)
        self.assertEquals(entry.module, module)
        self.assertEquals(entry.approved_by, self.user)

        # check methods of model for module aspects
        self.assertEquals(entry.module_code(), self.module.module_code)
        self.assertEquals(entry.module_name(), self.module.module_name)

        # check methods of model for approver aspects
        self.assertEquals(entry.approver_username(), self.user.username)
        self.assertEquals(entry.approver_name(), self.user.get_full_name())

    def test_model_one_to_many(self):
        """
        Unit test for checking that a module
        can have multiple entries in timeline.
        """
        title = "Test Changes"
        changes = "Test changes to report"
        status = "Finished",
        entry_type = "Random Entry"
        module = self.module

        en1 = TimelineEntry.objects.create(
            title=title,
            changes=changes,
            status=status,
            entry_type=entry_type,
            module=module,
            approved_by=self.user
        )

        en2 = TimelineEntry.objects.create(
            title=title,
            changes=changes,
            status=status,
            entry_type=entry_type,
            module=module,
            approved_by=self.user
        )

        n_entries = len(TimelineEntry.objects.filter(module=self.module))

        # includes extra entry from creating the test module
        self.assertEquals(n_entries, 3)

        # check they have the same module
        self.assertEquals(en1.module, en2.module)

    def test_module_cascade_delete(self):
        """
        Unit test for checking that model
        entries are deleted in module is deleted
        """
        title = "Test Changes"
        changes = "Test changes to report"
        status = "Draft",
        entry_type = "Generic"
        module = self.module

        entry = TimelineEntry.objects.create(
            title=title,
            changes=changes,
            status=status,
            entry_type=entry_type,
            module=module,
            approved_by=self.user
        )

        entry_id = entry.id

        # delete the module
        self.module.delete()

        # check that entry has been removed
        with self.assertRaises(TimelineEntry.DoesNotExist):
            TimelineEntry.objects.get(id=entry_id)

        # check that there are no entries
        n_entries = len(TimelineEntry.objects.filter(module=self.module))
        self.assertEquals(n_entries, 0)

    def test_model_no_approver(self):
        """
        Unit test for checking a entry can be made
        when no approver is provided.
        """
        title = "Test Changes"
        changes = "Test changes to report"
        status = "Draft",
        entry_type = "Generic"
        module = self.module

        entry = TimelineEntry.objects.create(
            title=title,
            changes=changes,
            status=status,
            entry_type=entry_type,
            module=module,
        )

        # check some attributes to check it has worked
        self.assertEquals(entry.title, title)
        self.assertEquals(entry.changes, changes)

        # check that approver methods return None
        self.assertEquals(entry.approver_username(), None)
        self.assertEquals(entry.approver_name(), None)

    def test_invlid_model_no_module(self):
        """
        Unit test for providing no module
        to create an entry
        """
        title = "Test Changes"
        changes = "Test changes to report"
        status = "Draft",
        entry_type = "Generic"

        # check with None parameter it
        # still triggers an exception.
        with self.assertRaises(IntegrityError):
            TimelineEntry.objects.create(
                title=title,
                changes=changes,
                status=status,
                entry_type=entry_type,
                module=None,
            )
