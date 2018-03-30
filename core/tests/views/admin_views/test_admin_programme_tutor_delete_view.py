from django.core.urlresolvers import reverse
from core.tests.views.admin_views.admin_test_case import AdminViewTestCase
from core.models import ProgrammeTutor


class TestAdminProgrammeTutorDeleteView(AdminViewTestCase):
    def setUp(self):
        super(TestAdminProgrammeTutorDeleteView, self).setUp()
        # finish this
