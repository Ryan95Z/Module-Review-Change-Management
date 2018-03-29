from django.db import models
from django.forms.models import model_to_dict
from timeline.utils.factory import EntryFactory


class BaseTimelineNode(models.Model):
    """
    Class to allow changes that are made to a model
    to be tracked.
    """
    created = models.DateTimeField(auto_now_add=True)
    is_new = False

    def __init__(self, *args, **kwargs):
        super(BaseTimelineNode, self).__init__(*args, **kwargs)
        self.base = model_to_dict(self)

    def title(self):
        """
        Returns the title that will be displayed
        on the timeline.
        """
        return self.__class__.__name__

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
        # INIT = "init" + self.__class__.__name__
        # UPDATE = "update" + self.__class__.__name__
        """
        Override standard save method of any model.
        Enables an entry to be made on the timeline
        each time a model instance is created or updated.
        """

        # optional kwargs argument that will force the changes
        # to not be placed on the timeline.
        # override_update = kwargs.pop('override_update', False)
        if not self.created:
            self.is_new = True
        #     # create an init entry
        #     super(BaseTimelineNode, self).save(*args, **kwargs)
        #     EntryFactory.makeEntry(INIT, self)
        #     return

        # if not override_update:
        #     # create an update entry
        #     EntryFactory.makeEntry(UPDATE, self)
        #     return

        # save the changes to database
        super(BaseTimelineNode, self).save(*args, **kwargs)

    class Meta:
        abstract = True
