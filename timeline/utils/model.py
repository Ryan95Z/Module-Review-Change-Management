from django.forms.models import model_to_dict


class ModelDifferance(object):
    """
    Class to allow changes that are made to a model
    to be tracked.
    """
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
        return bool(self.difference())
