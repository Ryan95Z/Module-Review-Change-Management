from .base_timeline_model_testcase import BaseTimelineModelTestCase
from django.db.utils import IntegrityError
from core.models import User, Module
from timeline.models import TimelineEntry


class TestTimelineEntry(BaseTimelineModelTestCase):
    """
    Test case for the TimelineEntry model
    """
    def setUp(self):
        super(TestTimelineEntry, self).setUp()
        self.model = TimelineEntry

    def test_create_valid_model(self):
        """
        Test for creating a valid model
        """
        title = "Test Changes"
        changes = "Test changes to report"
        status = "Draft",
        entry_type = "Generic"
        module = self.module

        entry = self.model.objects.create(
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
        Test for checking that a module
        can have multiple entries in timeline.
        """
        title = "Test Changes"
        changes = "Test changes to report"
        status = "Finished",
        entry_type = "Random Entry"
        module = self.module

        en1 = self.model.objects.create(
            title=title,
            changes=changes,
            status=status,
            entry_type=entry_type,
            module=module,
            approved_by=self.user
        )

        en2 = self.model.objects.create(
            title=title,
            changes=changes,
            status=status,
            entry_type=entry_type,
            module=module,
            approved_by=self.user
        )

        n_entries = len(self.model.objects.filter(module=self.module))

        # includes extra entry from creating the test module
        self.assertEquals(n_entries, 3)

        # check they have the same module
        self.assertEquals(en1.module, en2.module)

    def test_module_cascade_delete(self):
        """
        Test for checking that model
        entries are deleted in module is deleted
        """
        title = "Test Changes"
        changes = "Test changes to report"
        status = "Draft",
        entry_type = "Generic"
        module = self.module

        entry = self.model.objects.create(
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
        with self.assertRaises(self.model.DoesNotExist):
            self.model.objects.get(id=entry_id)

        # check that there are no entries
        n_entries = len(self.model.objects.filter(module=self.module))
        self.assertEquals(n_entries, 0)

    def test_model_no_approver(self):
        """
        Test for checking a entry can be made
        when no approver is provided.
        """
        title = "Test Changes"
        changes = "Test changes to report"
        status = "Draft",
        entry_type = "Generic"
        module = self.module

        entry = self.model.objects.create(
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
        Test for providing no module
        to create an entry
        """
        title = "Test Changes"
        changes = "Test changes to report"
        status = "Draft",
        entry_type = "Generic"

        # check with None parameter it
        # still triggers an exception.
        with self.assertRaises(IntegrityError):
            self.model.objects.create(
                title=title,
                changes=changes,
                status=status,
                entry_type=entry_type,
                module=None,
            )

    def test_valid_model_extreme_changes_data(self):
        """
        Test to ensure that changes attribute can support
        a large amount of data if required.
        """
        title = "Test Changes"
        status = "Draft",
        entry_type = "Generic"
        module = self.module
        changes = """
            Lorem ipsum dolor sit amet, consectetur adipiscing elit
            Mauris rutrum eget justo ac pulvinar. Cras dolor nunc, euismod
            tincidunt dignissim at, vestibulum nec tortor. Nunc et dolor
            rhoncus ipsum condimentum volutpat. Pellentesque pulvinar pharetra
            purus, ut cursus dui consectetur ac. Suspendisse et pharetra nunc.
            Praesent porta, tellus a rutrum rutrum, purus magna gravida dui,
            ut rhoncus sapien nisl nec nulla. Cras venenatis pharetra
            dignissim. Fusce finibus lorem in sem commodo, ac sagittis quam
            aliquam. Aenean justo ante, hendrerit ut sapien eget, tristique
            scelerisque tellus. Donec sed egestas nunc. Curabitur ut erat id
            puru malesuada ornare. Nullam a velit tempor dolor rutrum
            convallis. Integer sollicitudin ut tellus nec venenatis.
            Maecenas ac ullamcorper leo. Quisque vel augue non velit fringilla
             fringilla.
        """

        entry = self.model.objects.create(
            title=title,
            changes=changes,
            status=status,
            entry_type=entry_type,
            module=module,
        )

        self.maxDiff = None
        self.assertEquals(entry.changes, changes)
