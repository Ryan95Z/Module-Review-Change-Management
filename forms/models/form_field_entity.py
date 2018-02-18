from django.db import models

class FormFieldEntity(models.Model):
    """
    Represents an entity within a dynamic form
    """
    ENTITY_TYPE_OPTIONS = (
        ("text-input", "Text Input"),
        ("text-area", "Text Area"),
        ("multi-choice", "Select Box"),
        ("check-boxes", "Check Boxes")
    )

    entity_id = models.AutoField(primary_key=True)
    entity_title = models.CharField(max_length=50, verbose_name="Title/Label")
    entity_type = models.CharField(choices=ENTITY_TYPE_OPTIONS, max_length=12, verbose_name="Type")
    entity_description = models.CharField(blank=True, max_length=1000, verbose_name="Description")
    entity_placeholder = models.CharField(blank=True, max_length=100, verbose_name="Placeholder")
    entity_max_length = models.PositiveSmallIntegerField(default=100, verbose_name="Max Length")
    #version_hash = models.OneToOneField(FormHash)