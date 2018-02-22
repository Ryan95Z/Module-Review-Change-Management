from django.urls import reverse
from timeline.models import TimelineEntry
from .timeline_view_testcase import TimelineViewTestCase


class TimelineUpdateViewTest(TimelineViewTestCase):
    """
    Test case for the TimelineUpdateView.
    """
    def setUp(self):
        super(TimelineUpdateViewTest, self).setUp()
        kwargs = {
            'module_pk': self.module.module_code,
            'pk': self.entry.pk
        }
        self.url = reverse('entry_edit', kwargs=kwargs)

    def test_get_entry_update_view(self):
        """
        Test for getting the update view when the
        entry status is "Draft".
        """
        # check that the entry has the draft status
        self.assertEquals(self.entry.status, "Draft")

        context = self.run_get_view(self.url).context

        # check that the context is correct.
        self.assertEquals(context['title'], self.entry.title)
        self.assertEquals(context['pk'], self.entry.pk)
        self.assertEquals(context['module_code'], self.module.module_code)

    def test_get_entry_not_logged_in(self):
        """
        Test to ensure that view cannot be accessed
        unless user is logged in.
        """
        self.run_get_view_not_logged_in(self.url)

    def test_get_entry_with_other_entry_status(self):
        """
        Test for checking that a non-draft entry cannot
        access the view.
        """
        model = TimelineEntry
        kwargs = {'module_pk': self.module.module_code}
        redirect_url = reverse('module_timeline', kwargs=kwargs)

        # sample values for the entry
        title = "Test Entry"
        changes = "Minor changes to the module"
        # create first type as "Staged"
        status = "Staged"
        entry_type = "Generic"
        module = self.module.module_code

        # create the staged entry
        staged_entry = model.objects.create(
            title=title,
            changes=changes,
            status=status,
            entry_type=entry_type,
            module=self.module
        )

        # create the confirmed entry
        status = "Confirmed"
        confirmed_entry = model.objects.create(
            title=title,
            changes=changes,
            status=status,
            entry_type=entry_type,
            module=self.module
        )

        # assert that a "Staged" entry cannot be
        # edited. So redirected instead.
        kwargs = {
            'module_pk': self.module.module_code,
            'pk': staged_entry.pk
        }
        test_url = reverse('entry_edit', kwargs=kwargs)
        self.client.force_login(self.admin)
        response = self.client.get(test_url)

        self.assertEquals(response.status_code, 302)
        self.assertEquals(response.url, redirect_url)

        # assert that a "Confirmed" entry cannot be
        # edited. So redirected instead.
        kwargs = {
            'module_pk': self.module.module_code,
            'pk': confirmed_entry.pk
        }
        test_url = reverse('entry_edit', kwargs=kwargs)
        self.client.force_login(self.admin)
        response = self.client.get(test_url)

        self.assertEquals(response.status_code, 302)
        self.assertEquals(response.url, redirect_url)

    def test_valid_post_update(self):
        """
        Test case for providing valid data the the view.
        """
        changes = 'This is a new change to the module'
        data = {
            'changes': changes
        }

        model = TimelineEntry
        kwargs = {'module_pk': self.module.module_code}
        redirect_url = reverse('module_timeline', kwargs=kwargs)

        response = self.run_valid_post_view(self.url, data)
        self.assertEquals(response.url, redirect_url)

        # check that the model has been updated
        entry = model.objects.get(pk=self.entry.pk)
        self.assertEquals(entry.pk, self.entry.pk)
        self.assertEquals(entry.title, self.entry.title)
        self.assertEquals(entry.changes, changes)

    def test_invalid_post_update(self):
        """
        Test case for providing invalid data, which can only be
        empty data.
        """
        data = {
            'changes': ''
        }

        exptected_err = "['This field is required.']"

        context = self.run_invalid_post_view(self.url, data).context
        # check that the error was rasied
        form_errors = context['form'].errors.as_data()
        changes_err = form_errors['changes'][0].__str__()
        self.assertEquals(changes_err, exptected_err)

    def test_valid_post_update_extreme_data_cases(self):
        """
        Test case for asserting that other types of
        data are supported if provided, since it converts
        everything to a string automatically. Though this
        is high unlikely to occur.
        """
        model = TimelineEntry

        # test with a large int
        ch1 = 12949569594949
        data = {
            'changes': ch1
        }

        # test that change was sucessful
        self.run_valid_post_view(self.url, data)
        entry = model.objects.get(pk=self.entry.pk)
        self.assertEquals(entry.changes, str(ch1))

        # test it with an object
        data = {
            'changes': self.module
        }

        self.run_valid_post_view(self.url, data)
        entry = model.objects.get(pk=self.entry.pk)
        self.assertEquals(entry.changes, self.module.__str__())

        # assert that the view can handle a large amount of text data
        ch2 = """
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

        data = {
            'changes': ch2
        }

        self.run_valid_post_view(self.url, data)
        entry = model.objects.get(pk=self.entry.pk)

        # override the maxdiff for large text
        self.maxDiff = None
        self.assertEquals(entry.changes, ch2.strip())
