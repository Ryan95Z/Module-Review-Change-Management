from core.tests.common_test_utils import LoggedInTestCase, ModuleTestCase
from timeline.utils.notifications.helpers import WatcherWrapper
from timeline.utils.notifications.notices import BaseNotice
from timeline.models import Notification


class BaseTestNotification(LoggedInTestCase, ModuleTestCase):
    """
    Base Test case class for testing different notification classes
    """
    def setUp(self):
        super(BaseTestNotification, self).setUp()
        self.model = Notification
        self.watcher = WatcherWrapper(self.user)


class MockNotice(BaseNotice):
    """
    Mock class to test BaseNotice methods
    """
    def __init__(self, content_template, link_name):
        super(MockNotice, self).__init__(
            content_template=content_template,
            link_name=link_name
        )

    def factory(self):
        return self.__class__(self.content_template, self.link_name)

    def create(self, **kwargs):
        pass


class TestBaseNotice(BaseTestNotification):
    """
    Test case for the BaseNotice method using a mock model
    """

    def setUp(self):
        self.notice = MockNotice

    def test_notice_constructor(self):
        """
        Test the constructor of the base class
        """
        # test valid instantiation of object
        content_template = "Hello World"
        link_name = "Test"

        n = self.notice(content_template, link_name)
        self.assertEquals(n.content_template, content_template)
        self.assertEquals(n.link_name, link_name)

        # test with empty content template
        with self.assertRaises(ValueError):
            self.notice("", link_name)

        # test with empty link
        with self.assertRaises(ValueError):
            self.notice(content_template, "")

    def test_notice_factory(self):
        """
        Test case for creating objects from factory method
        """
        n = self.notice("Test", "Test")

        # get the object
        obj = n.factory()

        # test the object is correct
        self.assertEquals(n.__class__, obj.__class__)
        self.assertEquals(n.content_template, obj.content_template)
        self.assertEquals(n.link_name, obj.link_name)
        self.assertTrue(issubclass(obj.__class__, BaseNotice))
