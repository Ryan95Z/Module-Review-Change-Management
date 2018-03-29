from django.test import TestCase
# from timeline.utils.factory import EntryFactory
from timeline.tests.mocks import MockEntry, InvalidMockEntry
from timeline.register import timeline_register


class TestTimelineRegister(TestCase):
    """
    Test case for timeline_register decorator
    """
    pass

    # def test_successful_reigster(self):
    #     """
    #     Tests to ensure a model can be
    #     registered with the factory
    #     """
    #     model = MockEntry
    #     cls = timeline_register(model)
    #     self.assertEquals(cls, model)

    #     # check that the factory added the instances
    #     factory_classes = EntryFactory.assigned_instances()
    #     self.assertTrue(('initMockEntry' in factory_classes))
    #     self.assertTrue(('updateMockEntry' in factory_classes))

    # def test_unsuccessful_register(self):
    #     """
    #     Tests to check models that do not inherit
    #     the required model can be processed.
    #     """
    #     model = InvalidMockEntry

    #     with self.assertRaises(ValueError):
    #         timeline_register(model)
