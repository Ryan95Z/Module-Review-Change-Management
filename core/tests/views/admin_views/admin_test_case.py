from core.tests.common_test_utils import LoggedInTestCase


class AdminViewTestCase(LoggedInTestCase):
    """
    Base test case for admin views
    """
    def setUp(self):
        super(AdminViewTestCase, self).setUp()
        session = self.client.session
        session['username'] = self.admin.username
        session.save()

        self.admin_password = "password"
