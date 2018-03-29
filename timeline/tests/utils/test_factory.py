# from timeline.utils.factory import EntryFactory
# from timeline.utils.entries import InitEntry
# from core.models import Module
# from core.tests.common_test_utils import ModuleTestCase


# class TestEntryFactory(ModuleTestCase):
#     def setUp(self):
#         super(TestEntryFactory, self).setUp()
#         self.factory = EntryFactory

#     def test_factory_register(self):
#         alis = "factory1"
#         EntryFactory.register(InitEntry, alis, Module)

#         assigned_insts = EntryFactory.assigned_instances()
#         self.assertTrue((alis in assigned_insts))

#     def test_assigned_instances_default(self):
#         init_module = "initModule"
#         update_module = "updateModule"

#         assigned_insts = EntryFactory.assigned_instances()
#         self.assertTrue((init_module in assigned_insts))
#         self.assertTrue((update_module in assigned_insts))

#     def test_get_factory_with_alis(self):
#         alis = "factory1"
#         EntryFactory.register(InitEntry, alis, Module)

#         entry = EntryFactory.get(alis)
#         self.assertTrue(isinstance(entry, InitEntry))

#     def test_get_factory_with_invalid_alis(self):
#         alis = "rubbish"

#         with self.assertRaises(KeyError):
#             EntryFactory.get(alis)

#     def test_valid_make_entry(self):
#         alis = "factory1"
#         EntryFactory.register(InitEntry, alis, Module)

#         # test that it can actually make an entry
#         entry = EntryFactory.makeEntry(alis, self.module)
#         self.assertEquals(entry.module_code, self.module.module_code)

#     def test_invalid_make_entry(self):
#         aliases = ['rubbish', 38948585, None]

#         # test that exception is raised with different
#         # types of invlad keys
#         for alis in aliases:
#             with self.assertRaises(KeyError):
#                 EntryFactory.makeEntry(alis, self.module)

#         # test with a None instance
#         alis = "factory1"
#         EntryFactory.register(InitEntry, alis, Module)
#         with self.assertRaises(ValueError):
#             EntryFactory.makeEntry(alis, None)
