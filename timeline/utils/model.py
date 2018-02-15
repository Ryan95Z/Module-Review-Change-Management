from django.db import models
from django.forms.models import model_to_dict
from timeline.utils.factory import EntryFactory


class ModelDifferance(models.Model):
    """
    Class to allow changes that are made to a model
    to be tracked.
    """
    created = models.DateTimeField(auto_now_add=True)

    def __init__(self, *args, **kwargs):
        super(ModelDifferance, self).__init__(*args, **kwargs)
        self.base = {}
        if len(self.module_code) > 0:
            self.base = model_to_dict(self)

    def differences(self):
        """
        Returns dict of changes that have been made to an
        attribute. Value for each key contains a tuple with
        the orignal value and new value.
        """
        # convert the model to a dict
        current = model_to_dict(self)
        diff = {}

        if not bool(self.base):
            return diff

        # loop through each item in dict
        # and check for any changes
        for key, value in current.items():
            base_value = self.base[key]
            if base_value != value:
                diff[key] = (base_value, value)
        return diff

    def hasDifferences(self):
        """
        Returns boolean on if there are any changes.
        """
        return bool(self.differences())

    def save(self, *args, **kwargs):
        override_update = kwargs.pop('override_update', False)
        save_changes = True
        if not self.created:
            EntryFactory.makeEntry("init", self)
        else:
            if not override_update:
                EntryFactory.makeEntry("update", self)
                save_changes = not bool(self.hasDifferences())

        if save_changes:
            super(ModelDifferance, self).save(*args, **kwargs)

    class Meta:
        abstract = True
