from core.models import Module
from django.db.models.signals import post_save
from django.dispatch import receiver

from timeline.utils.factory import EntryFactory


@receiver(post_save, sender=Module)
def module_created(sender, instance, created, **kwargs):
    if created:
        EntryFactory.makeEntry("init", instance)


@receiver(post_save, sender=Module)
def module_update(sender, instance, **kwargs):
    EntryFactory.makeEntry("update", instance)
