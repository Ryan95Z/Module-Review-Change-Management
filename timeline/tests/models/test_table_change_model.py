from django.db.utils import IntegrityError
from core.models import User, Module
from timeline.models import TimelineEntry, TableChange
from .base_timeline_model_testcase import BaseTimelineModelTestCase


class TestTableChange(BaseTimelineModelTestCase):
    """
    Test case for the TableChange model
    """
    def setUp(self):
        super(TestTableChange, self).setUp()

        self.entry = TimelineEntry.objects.create(
            title="Test Changes",
            changes="Test changes to report",
            status="Draft",
            entry_type="Generic",
            module=self.module,
            approved_by=self.user
        )

        self.model = TableChange

    def test_create_valid_model(self):
        """
        Unit test for creating a model
        """
        model = "Module"
        model_id = self.module.module_code
        changes_field = "module_code"
        current_value = self.module.module_code
        new_value = "CM1243"
        related_entry = self.entry

        changes = self.model.objects.create(
            changes_for_model=model,
            model_id=model_id,
            changes_field=changes_field,
            current_value=current_value,
            new_value=new_value,
            related_entry=related_entry
        )

        # check attributes
        self.assertEquals(changes.changes_for_model, model)
        self.assertEquals(changes.model_id, model_id)
        self.assertEquals(changes.changes_field, changes_field)
        self.assertEquals(changes.current_value, current_value)
        self.assertEquals(changes.new_value, new_value)
        self.assertEquals(changes.related_entry, related_entry)

        # check methods
        self.assertEquals(
            changes.related_module_code(), self.module.module_code)

    def test_model_cascade_entry_delete(self):
        """
        Unit test for ensuring that changes in table
        in the related entry is deleted.
        """
        model = "Module"
        model_id = self.module.module_code
        changes_field = "module_code"
        current_value = self.module.module_code
        new_value = "CM1243"
        related_entry = self.entry

        change = self.model.objects.create(
            changes_for_model=model,
            model_id=model_id,
            changes_field=changes_field,
            current_value=current_value,
            new_value=new_value,
            related_entry=related_entry
        )

        change_id = change.id

        # check that the entry is assigned
        self.assertEquals(change.related_entry, self.entry)

        # delete entry
        self.entry.delete()

        # check it has been removed
        with self.assertRaises(self.model.DoesNotExist):
            self.model.objects.get(id=change_id)

    def test_model_casade_module_delete(self):
        """
        Unit test to ensure that if the module
        is deleted, the cascaded entry deletion
        will also affect TableChange.
        """
        model = "Module"
        model_id = self.module.module_code
        changes_field = "module_code"
        current_value = self.module.module_code
        new_value = "CM1243"
        related_entry = self.entry

        change = self.model.objects.create(
            changes_for_model=model,
            model_id=model_id,
            changes_field=changes_field,
            current_value=current_value,
            new_value=new_value,
            related_entry=related_entry
        )

        change_id = change.id

        # delete module
        self.module.delete()

        # check it has been removed
        with self.assertRaises(self.model.DoesNotExist):
            self.model.objects.get(id=change_id)

    def test_invalid_model_null_entry(self):
        """
        Unit test to ensure model cannot be created
        if an entry is not assigned to it.
        """
        model = "Module"
        model_id = self.module.module_code
        changes_field = "module_code"
        current_value = self.module.module_code
        new_value = "CM1243"
        related_entry = None

        # check the exception is raised
        with self.assertRaises(IntegrityError):
            self.model.objects.create(
                changes_for_model=model,
                model_id=model_id,
                changes_field=changes_field,
                current_value=current_value,
                new_value=new_value,
                related_entry=related_entry
            )
