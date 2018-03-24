from core.tests.common_test_utils import LoggedInTestCase, ModuleTestCase
from timeline.utils.notifications.helpers import WatcherWrapper
from core.models import Module


class TestWatcherWrapper(LoggedInTestCase, ModuleTestCase):
    def setUp(self):
        super(TestWatcherWrapper, self).setUp()
        self.obj = WatcherWrapper

    def test_adding_modules(self):
        """
        Test the method to add modules to the watcher wrapper
        """
        watcher = self.obj(self.user)
        self.assertEquals(watcher.user, self.user)

        # check that no modules are assigned
        self.assertEquals(watcher.modules().count(), 0)

        # add module by Module object
        added = watcher.add_module(self.module)
        self.assertTrue(added)
        self.assertEquals(watcher.modules().count(), 1)

        # add module by module code
        added = watcher.add_module(self.module_two.module_code)
        self.assertTrue(added)
        self.assertEquals(watcher.modules().count(), 2)

    def test_removing_modules(self):
        """
        Test the method to remove modules to the watcher wrapper
        """
        watcher = self.obj(self.user)
        self.assertEquals(watcher.user, self.user)
        watcher.add_module(self.module)
        watcher.add_module(self.module_two)

        # check modules have been added
        self.assertEquals(watcher.modules().count(), 2)

        # remove the module by Module object
        removed = watcher.remove_module(self.module)
        self.assertTrue(removed)
        self.assertEquals(watcher.modules().count(), 1)

        # remove the module by module code
        removed = watcher.remove_module(self.module_two.module_code)
        self.assertTrue(removed)
        self.assertEquals(watcher.modules().count(), 0)

    def test_add_modules_invalid_data(self):
        watcher = self.obj(self.user)
        module_list = list(Module.objects.all())
        watcher.bulk_module_add(*module_list)
        self.assertEquals(watcher.modules().count(), 2)
