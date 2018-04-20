from django.urls import reverse
from .timeline_view_testcase import TimelineViewTestCase


class TestTrackingFormChangesView(TimelineViewTestCase):
    """
    Test case for the TrackingFormChanges view
    """
    def setUp(self):
        super(TestTrackingFormChangesView, self).setUp()
        self.c1 = self.model.objects.create(
            title="Test Child 1",
            changes="Test changes to report",
            status="Draft",
            entry_type="Generic",
            module_code=self.module.module_code,
            object_id=self.module.module_code,
            content_object=self.module,
            changes_by=self.user,
            parent_entry=self.entry
        )

        self.c2 = self.model.objects.create(
            title="Test Child 2",
            changes="Test changes to report",
            status="Draft",
            entry_type="Generic",
            module_code=self.module.module_code,
            object_id=self.module.module_code,
            content_object=self.module,
            changes_by=self.user,
            parent_entry=self.entry
        )

        self.url = reverse('changes', kwargs={
            'module_pk': self.module.module_code,
            'pk': self.entry.pk
        })

    def test_get_form_change(self):
        """
        Test to get the view correctly
        """
        context = self.run_get_view(self.url).context
        self.assertEqual(context['parent'], self.entry)
        self.assertEqual(context['entries'].count(), 2)
        self.assertEqual(context['module_code'], self.module.module_code)

    def test_get_form_changes_invalid_user(self):
        """
        Test to ensure that non-logged in users can access the view
        """
        self.run_get_view_not_logged_in(self.url)

    def test_get_form_raise_404(self):
        """
        Test case to assert 404 is raised under certain conditions
        """
        # fake entry for testing the parent
        fake_parent = self.model.objects.create(
            title="Test Child 2",
            changes="Test changes to report",
            status="Draft",
            entry_type="Generic",
            module_code=self.module.module_code,
            object_id=self.module.module_code,
            content_object=self.module,
            changes_by=self.user,
        )

        url = reverse('changes', kwargs={
            'module_pk': self.module.module_code,
            'pk': 404
        })

        self.client.force_login(self.admin)

        # test with invalid parent id
        response = self.client.get(url)
        self.assertEquals(response.status_code, 404)

        # test it with a entry with no children
        url = reverse('changes', kwargs={
            'module_pk': self.module.module_code,
            'pk': fake_parent.pk
        })

        response = self.client.get(url)
        self.assertEquals(response.status_code, 404)
