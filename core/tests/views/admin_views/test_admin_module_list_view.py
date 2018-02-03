from django.core.urlresolvers import reverse
from core.tests.views.admin_views.admin_test_case import AdminViewTestCase
from core.models import Module


class TestAdminModuleListView(AdminViewTestCase):
    """
    Unit test for AdminModuleListView
    """

    def setUp(self):
        super(TestAdminModuleListView, self).setUp()
        self.url = reverse('all_modules')

    def test_get_module_list_view(self):
        """
        Test case for accessing the view as an admin
        """
        self.run_get_view(self.url)

    def test_get_module_list_view_with_incorrect_access(self):
        """
        Test case to check non-admin users accessing the view
        """
        self.run_get_view_incorrect_access(self.url)

    def test_get_module_list_view_not_logged_in(self):
        """
        Test case to check that non-logged in users cannot access the view
        """
        self.run_get_view_not_logged_in(self.url)

    def test_get_module_list_with_search(self):
        # create a 3 modules to test search
        Module.objects.create(
            module_code="CM3301",
            module_name="Software Engineering Project",
            module_credits=40,
            module_level="L3",
            module_year="Year 3",
            semester="Double Semester",
            delivery_language="English",
            module_leader=self.user
        )

        Module.objects.create(
            module_code="CM3202",
            module_name="Emerging Technologies",
            module_credits=20,
            module_level="L3",
            module_year="Year 3",
            semester="Sprint Semester",
            delivery_language="English",
            module_leader=self.user
        )

        Module.objects.create(
            module_code="CM3201",
            module_name="Project and Change Management",
            module_credits=20,
            module_level="L3",
            module_year="Year 3",
            semester="Sprint Semester",
            delivery_language="English",
            module_leader=self.user
        )

        # assert that without the search GET param
        # we still get all 3 modules
        object_list = self.run_get_view(self.url).context['object_list']
        self.assertEquals(3, object_list.count())

        # search for modules that have "CM32" in the module code
        search = "CM32"
        response = self.client.get(self.url, {'search': search})
        self.assertEquals(response.status_code, 200)

        # assert 2 are only returned
        object_list = response.context['object_list']
        self.assertEquals(2, object_list.count())

        # search for a specific module based on the name
        search = "Emerging Technologies"
        response = self.client.get(self.url, {'search': search})
        self.assertEquals(response.status_code, 200)

        object_list = response.context['object_list']
        # assert 1 is only returned
        self.assertEquals(1, object_list.count())
