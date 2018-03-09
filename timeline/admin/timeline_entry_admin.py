from django.contrib import admin
from timeline.models import TimelineEntry


class TimelineEntryAdmin(admin.ModelAdmin):
    """
    Class for creating the admin interface for the
    TimelineEntry model when viewed in the generated
    Django interface.
    """

    list_display = ('pk', 'title', 'changes')

    ordering = ('created', )

    # def get_form(self, request, obj=None, **kwargs):
    #     """
    #     Method to override the generated form
    #     for the Django Admin.
    #     """

    #     # remove the approved_by field
    #     self.exclude = ('approved_by', )
    #     form = super(TimelineEntryAdmin, self).get_form(request, obj, **kwargs)
    #     return form


admin.site.register(TimelineEntry, TimelineEntryAdmin)
