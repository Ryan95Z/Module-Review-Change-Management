from django.contrib import admin
from timeline.models import TimelineEntry


class TimelineEntryAdmin(admin.ModelAdmin):
    list_display = ('title', 'changes', 'module')

    ordering = ('created', )

admin.site.register(TimelineEntry, TimelineEntryAdmin)
