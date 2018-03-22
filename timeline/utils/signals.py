from core.models import Module
from timeline.models import TimelineEntry
from django.db.models.signals import pre_delete
from django.dispatch import receiver


@receiver(pre_delete, sender=Module)
def timeline_clearup(sender, instance, **kwargs):
    mc = instance.module_code
    TimelineEntry.objects.filter(module_code=mc).delete()

# @receiver(post_save, sender=Module)
# def module_created(sender, instance, created, **kwargs):
#     if created:
#         EntryFactory.makeEntry("init", instance)


# @receiver(post_save, sender=Module)
# def module_update(sender, instance, **kwargs):
#     EntryFactory.makeEntry("update", instance)
