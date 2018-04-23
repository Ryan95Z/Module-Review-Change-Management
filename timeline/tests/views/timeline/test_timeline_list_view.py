from .timeline_view_testcase import TimelineViewTestCase
from django.core.urlresolvers import reverse


class TimelineListViewTest(TimelineViewTestCase):
    """
    Test for case testing the TimelineListView
    """
    def setUp(self):
        super(TimelineListViewTest, self).setUp()

        kwargs = {'module_pk': self.module.module_code}
        self.url = reverse('module_timeline', kwargs=kwargs)

    def test_get_timeline_list_view(self):
        """
        Test case for accessing the view as expected
        """

        # assert we can get the view successfully
        # then get the context from the returned response
        context = self.run_get_view(self.url).context

        # check that the context is correct
        self.assertEquals(context['module_code'], self.module.module_code)

        # ensure there is two entries for the module.
        # One for creating the module, and another entry
        # that is created from the super class.
        self.assertEquals(len(context['object_list']), 1)
        self.assertTrue(context['block_pagination'])

    def test_get_timeline_list_view_not_logged_in(self):
        """
        Test case for checking that a user cannot access
        the view unless they are logged in.
        """
        self.run_get_view_not_logged_in(self.url)
