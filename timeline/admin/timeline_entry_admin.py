from django.contrib import admin
from timeline.models import TimelineEntry


class TimelineEntryAdmin(admin.ModelAdmin):
    list_display = ('title', 'changes', 'creator', 'module')

    ordering = ('created', )

    def creator(self, obj):
        return obj.created_by_username()


admin.site.register(TimelineEntry, TimelineEntryAdmin)
