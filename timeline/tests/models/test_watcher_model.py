from timeline.models import Watcher
from .base_timeline_model_testcase import BaseTimelineModelTestCase


class TestWatcher(BaseTimelineModelTestCase):
    def setUp(self):
        super(TestWatcher, self).setUp()
        self.model = Watcher

    def test_create_valid_model(self):
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
