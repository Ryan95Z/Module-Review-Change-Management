from django.core.management import call_command
from core.tests.common_test_utils import LoggedInTestCase, ModuleTestCase
from timeline.models import TimelineEntry
from timeline.utils.timeline.changes import revert_changes
from forms.models.tracking_form import ModuleTeaching


class TestRevertChanges(LoggedInTestCase, ModuleTestCase):
    def setUp(self):
        super(TestRevertChanges, self).setUp()
        self.master = ModuleTeaching(**{
            "module": self.module,
            "teaching_lectures": 45,
            "teaching_tutorials": 3,
            "teaching_online": 45,
            "teaching_practical_workshops": 8,
            "teaching_supervised_time": 8,
            "teaching_fieldworks": 8,
            "teaching_external_visits": 8,
            "teaching_schedule_assessment": 8,
            "teaching_placement": 8,
            "archive_flag": False,
            "staging_flag": True,
            "current_flag": False,
            "version_number": 1,
            "copy_number": 3
        })
        self.master.save()

        self.prev = ModuleTeaching(**{
            "module": self.module,
            "teaching_lectures": 8,
            "teaching_tutorials": 8,
            "teaching_online": 8,
            "teaching_practical_workshops": 8,
            "teaching_supervised_time": 8,
            "teaching_fieldworks": 8,
            "teaching_external_visits": 8,
            "teaching_schedule_assessment": 8,
            "teaching_placement": 8,
            "archive_flag": True,
            "staging_flag": False,
            "current_flag": False,
            "version_number": 2,
            "copy_number": 1
        })
        self.prev.save()

        self.current = ModuleTeaching(**{
            "module": self.module,
            "teaching_lectures": 45,
            "teaching_tutorials": 84,
            "teaching_online": 8,
            "teaching_practical_workshops": 8,
            "teaching_supervised_time": 8,
            "teaching_fieldworks": 8,
            "teaching_external_visits": 8,
            "teaching_schedule_assessment": 8,
            "teaching_placement": 8,
            "archive_flag": True,
            "staging_flag": False,
            "current_flag": False,
            "version_number": 3,
            "copy_number": 2
        })

        self.current.save()

        self.parent_entry = TimelineEntry(**{
            "title": "Changes to tracking form",
            "changes": "Changes to tracking form:\n\n* There are 1 changes to Module Teaching\n* There are 2 changes to Assessment test4\n* There are 1 changes to Software tet\n",
            "created": "2018-04-11T16:58:40.999Z",
            "last_modified": "2018-04-11T16:58:40.999Z",
            "module_code": self.module.module_code,
            "parent_entry": None,
            "status": "Draft",
            "entry_type": "Tracking-Form",
            "content_type": None,
            "object_id": None,
            "revert_object_id": "0",
            "changes_by": self.admin,
            "approved_by": None
        })
        self.parent_entry.save()

        self.entry = TimelineEntry(**{
            "title": "Module Teaching",
            "changes": "* teaching online: 8 -> 45\n",
            "created": "2018-04-11T16:58:41.019Z",
            "last_modified": "2018-04-11T16:58:41.019Z",
            "module_code": self.module.module_code,
            "parent_entry": self.parent_entry,
            "status": "Draft",
            "entry_type": "Tracking-Form",
            "content_object": self.current,
            "revert_object_id": self.prev.pk,
            "changes_by": None,
            "approved_by": None
        })
        self.entry.save()

    def test_valid_revert_changes(self):
        """
        Test that the changes are reverted for tracking form data
        """
        # test the current staged changes
        master = ModuleTeaching.objects.filter(version_number=1).first()
        self.assertTrue(master.staging_flag)
        self.assertFalse(master.archive_flag)
        self.assertFalse(master.current_flag)
        self.assertEquals(master.copy_number, 3)

        result = revert_changes(self.parent_entry)
        self.assertTrue(result)

        # check timeline has been removed
        with self.assertRaises(TimelineEntry.DoesNotExist):
            TimelineEntry.objects.get(pk=self.parent_entry.pk)

        # check that it has been reverted
        master = ModuleTeaching.objects.filter(version_number=1).first()
        self.assertTrue(master.current_flag)
        self.assertFalse(master.archive_flag)
        self.assertFalse(master.staging_flag)
        self.assertEquals(master.copy_number, 2)

    def test_no_children_master(self):
        """
        Test when there are no child for parent entry
        """
        result = revert_changes(self.entry)
        self.assertFalse(result)

    def test_invalid_master_instance(self):
        """
        Test when the parent entry is not a timeline entry type
        """
        parents = [None, ModuleTeaching, self.user]

        for parent in parents:
            with self.assertRaises(ValueError):
                revert_changes(parent)
