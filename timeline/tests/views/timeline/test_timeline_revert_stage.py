from django.urls import reverse
from forms.models.tracking_form import ModuleTeaching
from .timeline_view_testcase import TimelineViewTestCase


class TestTimelineRevertStage(TimelineViewTestCase):
    """
    Test case for TimelineRevertStage view
    """
    def setUp(self):
        super(TestTimelineRevertStage, self).setUp()
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

        self.parent_entry = self.model(**{
            "title": "Changes to tracking form",
            "changes": "Changes to tracking form:\n\n* There are 1 changes to Module Teaching\n* There are 2 changes to Assessment test4\n* There are 1 changes to Software tet\n",
            "created": "2018-04-11T16:58:40.999Z",
            "last_modified": "2018-04-11T16:58:40.999Z",
            "module_code": self.module.module_code,
            "parent_entry": None,
            "status": "Staged",
            "entry_type": "Tracking-Form",
            "content_type": None,
            "object_id": None,
            "revert_object_id": "0",
            "changes_by": self.admin,
            "approved_by": None
        })
        self.parent_entry.save()

        self.entry = self.model(**{
            "title": "Module Teaching",
            "changes": "* teaching online: 8 -> 45\n",
            "created": "2018-04-11T16:58:41.019Z",
            "last_modified": "2018-04-11T16:58:41.019Z",
            "module_code": self.module.module_code,
            "parent_entry": self.parent_entry,
            "status": "Staged",
            "entry_type": "Tracking-Form",
            "content_object": self.current,
            "revert_object_id": self.prev.pk,
            "changes_by": None,
            "approved_by": None
        })
        self.entry.save()

        self.url = reverse('revert_entry', kwargs={
            'module_pk': self.module.module_code,
            'pk': self.parent_entry.pk
        })

        self.response_url = reverse('module_timeline', kwargs={
            'module_pk': self.module.module_code
        })

    def test_revert_timeline_changes(self):
        """
        Test case for ensuring that changes are reverted
        at different workflow statuses
        """
        data = {
            'pk': self.parent_entry.pk
        }

        # test a revert when the parent is in staged status
        response = self.run_valid_post_view(self.url, data)
        self.assertEquals(response.url, self.response_url)

        updated_entry = self.model.objects.get(pk=self.parent_entry.pk)
        self.assertEquals(updated_entry.status, "Draft")

        # test revert with a parent in draft status
        response = self.run_valid_post_view(self.url, data)
        self.assertEquals(response.url, self.response_url)

        # entry should not have been deleted
        with self.assertRaises(self.model.DoesNotExist):
            self.model.objects.get(pk=self.parent_entry.pk)

    def test_revert_timeline_raise_404(self):
        """
        Test case to ensure that 404 is raised if invalid
        """
        url = reverse('revert_entry', kwargs={
            'module_pk': self.module.module_code,
            'pk': 404
        })

        data = {
            'pk': 404
        }

        self.client.force_login(self.admin)

        # test with invalid parent id
        response = self.client.post(url, data)
        self.assertEquals(response.status_code, 404)

    def test_get_view_redirect(self):
        """
        Test case to ensure client is redirected if
        they use the GET HTTP method.
        """
        self.client.force_login(self.admin)
        response = self.client.get(self.url)
        self.assertEquals(response.status_code, 302)
        self.assertEquals(response.url, self.response_url)

    def test_get_view_not_logged_in(self):
        """
        Test case to ensure view cannot be accessed in not logged in.
        """
        self.run_get_view_not_logged_in(self.url)
