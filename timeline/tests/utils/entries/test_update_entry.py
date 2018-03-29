# from core.models import Module, User
# from core.tests.common_test_utils import ModuleTestCase
# from timeline.models import TimelineEntry, TableChange


# class TestUpdatedEntry(ModuleTestCase):
#     """
#     Test cases for UpdatedEntry object
#     """
#     def setUp(self):
#         super(TestUpdatedEntry, self).setUp()
#         self.entry = UpdatedEntry
#         self.model = Module

#     def test_creating_valid_entry(self):
#         """
#         Test case for creating a valid update entry
#         """
#         updated_entry = self.entry(self.model)
#         self.assertEquals(updated_entry.title, "Changes to {}\n\n")
#         self.assertEquals(updated_entry.type, "Update")
#         self.assertEquals(updated_entry.model, self.model)
#         self.assertEquals(updated_entry.model_app_label, "core")

#         self.module.module_name = "Updated title"
#         self.module.module_credits = 36
#         self.module.save()

#         # check that the timeline entry is created
#         timeline_entry = updated_entry.create(self.module)
#         self.assertEquals(
#             timeline_entry.title,
#             updated_entry.title.format(self.module.title())
#         )

#         self.assertEquals(timeline_entry.status, "Draft")
#         self.assertEquals(timeline_entry.module_code, self.module.module_code)
#         self.assertEquals(timeline_entry.object_id, self.module.pk)
#         self.assertEquals(timeline_entry.entry_type, updated_entry.type)

#         # check it is in the database
#         db_timeline_entry = TimelineEntry.objects.get(id=timeline_entry.id)
#         self.assertTrue(db_timeline_entry is not None)

#     def test_assigning_entry_invalid_model(self):
#         """
#         Test case to enusre invalid models are not accepted
#         """

#         # check iwht None value
#         with self.assertRaises(ValueError):
#             self.entry(None)

#         # check with invalid model
#         with self.assertRaises(ValueError):
#             self.entry(User)

#     def test_entry_factroy(self):
#         """
#         Test case for checking that the factory creates
#         new instances.
#         """
#         updated_entry = self.entry(self.model)
#         new_updated_entry = updated_entry.factory()

#         self.assertTrue(new_updated_entry != updated_entry)
#         self.assertEquals(new_updated_entry.title, "Changes to {}\n\n")
#         self.assertEquals(new_updated_entry.type, "Update")
#         self.assertEquals(new_updated_entry.model, self.model)
#         self.assertEquals(new_updated_entry.model_app_label, "core")

#     def test_invalid_create_entry(self):
#         """
#         Test case for ensuring only valid instances
#         will be processed.
#         """
#         init_entry = self.entry(self.model)

#         with self.assertRaises(ValueError):
#             init_entry.create(None)

#         with self.assertRaises(ValueError):
#             init_entry.create(self.module_leader)
