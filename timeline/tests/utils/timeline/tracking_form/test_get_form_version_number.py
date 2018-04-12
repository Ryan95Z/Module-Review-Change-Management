from core.tests.common_test_utils import LoggedInTestCase, ModuleTestCase
from timeline.utils.timeline.tracking_form import get_form_version_number
from timeline.models import TimelineEntry
from forms.models.tracking_form import ModuleTeaching


class TestGetFormVersionNumber(LoggedInTestCase, ModuleTestCase):
    """
    Test case for the function get_form_version_number
    """
    def setUp(self):
        super(TestGetFormVersionNumber, self).setUp()

        self.function = get_form_version_number
        self.model = TimelineEntry

        self.master = ModuleTeaching.objects.create(**{
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

        self.prev = ModuleTeaching.objects.create(**{
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

        self.current = ModuleTeaching.objects.create(**{
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

        self.parent_entry = self.model.objects.create(**{
            "title": "Changes to tracking form",
            "changes": "Changes have been made",
            "created": "2018-04-11T16:58:40.999Z",
            "last_modified": "2018-04-11T16:58:40.999Z",
            "module_code": self.module.module_code,
            "parent_entry": None,
            "status": "Draft",
            "entry_type": "Tracking-Form",
            "content_object": None,
            "revert_object_id": "0",
            "changes_by": self.admin,
            "approved_by": None
        })

        self.entry = self.model.objects.create(**{
            "title": "Module Teaching",
            "changes": "* teaching online: 8 -> 45\n",
            "module_code": self.module.module_code,
            "parent_entry": self.parent_entry,
            "status": "Draft",
            "entry_type": "Tracking-Form",
            "object_id": self.current.pk,
            "content_object": self.current,
            "revert_object_id": self.prev.pk,
            "changes_by": None
        })

    def test_get_next_version_number(self):
        """
        Test function returns the version number
        based on the parent id
        """
        result = self.function(self.parent_entry.pk)
        self.assertEquals(result, 2)
