from timeline.models.integrate.entry import TLEntry
from django.db import models


class MockEntry(TLEntry):
    class Meta:
        app_label = "test_timeline"


class InvalidMockEntry(models.Model):
    class Meta:
        app_label = "test_timeline"
