from core.tests.common_test_utils import LoggedInTestCase, ModuleTestCase
from timeline.utils.notifications.helpers import WatcherWrapper
from core.models import Module


class TestWatcherWrapper(LoggedInTestCase, ModuleTestCase):
    """
    Tests for WatcherWrapper helper class
    """
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

    def test_bulk_modules_methods(self):
        """
        Test case for adding and removing a
        number of modules in one call.
        """
        watcher = self.obj(self.user)

        # get test modules
        module_list = list(Module.objects.all())

        # test adding modules
        output = watcher.bulk_module_add(*module_list)
        self.assertTrue(output)
        self.assertEquals(watcher.modules().count(), 2)

        # test removing modules
        output = watcher.bulk_module_remove(*module_list)
        self.assertTrue(output)
        self.assertEquals(watcher.modules().count(), 0)

    def test_wrapper_incorrect_types(self):
        """
        Test for ensuring that incorrect data types are
        not processed for certain methods.
        """
        # incorrect data for the constructor
        incorrect_data_list = ["user", 1234, self.module]
        for data in incorrect_data_list:
            with self.assertRaises(ValueError):
                WatcherWrapper(data)

        watcher = self.obj(self.user)

        # test incorrect data for add and remove single modules
        incorrect_data_list = [234646, 2.334, self.user]
        for data in incorrect_data_list:
            with self.assertRaises(ValueError):
                watcher.add_module(data)

            with self.assertRaises(ValueError):
                watcher.remove_module(data)

    def test_moudle_does_not_exist(self):
        """
        Test add and remove single module methods
        when a module code that doesn't exist is provided.
        """
        watcher = self.obj(self.user)

        # module code that does not exist
        module_code = "CM3301"

        output = watcher.add_module(module_code)
        self.assertFalse(output)

        output = watcher.remove_module(module_code)
        self.assertFalse(output)
