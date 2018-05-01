from django.db import models
from django.forms.models import model_to_dict


class BaseTimelineNode(models.Model):
    """
    Class to allow changes that are made to a model
    to be tracked.
    """
    created = models.DateTimeField(auto_now_add=True)

    def __init__(self, *args, **kwargs):
        super(BaseTimelineNode, self).__init__(*args, **kwargs)
        self.base = model_to_dict(self)
        self.is_new = False

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
        if not self.created:
            self.is_new = True
        super(BaseTimelineNode, self).save(*args, **kwargs)

    class Meta:
        abstract = True
