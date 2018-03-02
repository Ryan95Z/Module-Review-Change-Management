from django.db import models

from forms.models.module_description import ModuleDescriptionFormVersion

class FormFieldEntityManager(models.Manager):
    """
    Manager for the form field entity model
    """
    def get_most_recent_form(self):
        newest_version = ModuleDescriptionFormVersion.objects.get_most_recent()
        newest_version_fields = self.filter(
            module_description_version=newest_version
        ).order_by('entity_order').values()
        return newest_version_fields

    def get_form(self, version):
        chosen_version_fields = self.filter(
            module_description_version=version
        ).order_by('entity_order').values()
        return chosen_version_fields

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
    entity_order = models.PositiveSmallIntegerField()
    entity_label = models.CharField(max_length=50, verbose_name="Title/Label")
    entity_type = models.CharField(choices=ENTITY_TYPE_OPTIONS, max_length=12, verbose_name="Field Type")
    entity_choices = models.CharField(blank=True, max_length=100, verbose_name="Choices")
    entity_default = models.CharField(blank=True, max_length=100, verbose_name="Default")
    entity_description = models.CharField(blank=True, max_length=1000, verbose_name="Description")
    entity_placeholder = models.CharField(blank=True, max_length=100, verbose_name="Placeholder")
    entity_max_length = models.PositiveSmallIntegerField(default=500, verbose_name="Max Length")
    module_description_version = models.ForeignKey(ModuleDescriptionFormVersion)

    objects = FormFieldEntityManager()

    class Meta:
        ordering = ['entity_order']

    def __str__(self):
        return "FormFieldEntity: {} ({})".format(self.entity_label, self.entity_type)