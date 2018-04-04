from django.contrib import admin
from forms.models import *

# Register your models here.
admin.site.register(ModuleChangeSummary)
admin.site.register(ModuleTeaching)
admin.site.register(ModuleSupport)
admin.site.register(ModuleAssessment)
admin.site.register(ModuleReassessment)
admin.site.register(ModuleSoftware)

admin.site.register(FormFieldEntity)
admin.site.register(ModuleDescriptionFormVersion)
admin.site.register(ModuleDescription)
admin.site.register(ModuleDescriptionEntry)