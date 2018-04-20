from django.db import IntegrityError
from timeline.models import Watcher
from .base_timeline_model_testcase import BaseTimelineModelTestCase


class TestWatcher(BaseTimelineModelTestCase):
    """
    Test for Watcher model
    """
    def setUp(self):
        super(TestWatcher, self).setUp()
        self.model = Watcher

    def test_create_valid_model(self):
        """
        Creation of a valid watcher
        """
        watcher = self.model.objects.create(
            user=self.user
        )
        watcher.watching.add(self.module)

        # test the user
        self.assertEquals(watcher.user, self.user)
        self.assertEquals(watcher.watcher_username(), self.user.username)
        self.assertEquals(
            watcher.watcher_fullname(),
            self.user.get_full_name()
        )

        # test the module that was stored
        modules = watcher.watching.all()
        self.assertEquals(modules.count(), 1)

        module = modules[0]
        self.assertEquals(module.module_code, self.module.module_code)
        self.assertEquals(module.module_name, self.module.module_name)
        self.assertEquals(module.module_credits, self.module.module_credits)
        self.assertEquals(module.module_level, self.module.module_level)
        self.assertEquals(module.semester, self.module.semester)
        self.assertEquals(
            module.delivery_language,
            self.module.delivery_language
        )
        self.assertEquals(module.module_leader, self.user)

    def test_create_model_with_already_assigned_user(self):
        """
        Test that integrity error is raised if user that
        already has a model is assigned again.
        """
        # create the initial instance
        self.model.objects.create(user=self.user)

        # do it again, but check it cannot be done
        with self.assertRaises(IntegrityError):
            self.model.objects.create(user=self.user)

    def test_modules_delete_in_watcher(self):
        """
        Test to check watcher automatically removes
        modules that are deleted.
        """
        watcher = self.model.objects.create(
            user=self.user
        )
        watcher.watching.add(self.module)

        # check module has been added
        modules = watcher.watching.all()
        self.assertEquals(modules.count(), 1)

        # delete the module
        self.module.delete()

        # test the module has been removed
        modules = watcher.watching.all()
        self.assertEquals(modules.count(), 0)

    def test_watcher_delete_when_user_is(self):
        # add the watcher to db
        self.model.objects.create(user=self.user)

        # get the watcher and test to check it is
        watcher = self.model.objects.get(user=self.user)
        self.assertEquals(watcher.user, self.user)
        self.assertEquals(watcher.watcher_username(), self.user.username)

        # delete the user
        self.user.delete()

        # not check it has been removed
        with self.assertRaises(self.model.DoesNotExist):
            self.model.objects.get(user=self.user)
