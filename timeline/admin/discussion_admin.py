from django.contrib import admin
from timeline.models import Discussion


class DiscussionAdmin(admin.ModelAdmin):
    list_display = ('pk', 'author', 'created')


admin.site.register(Discussion, DiscussionAdmin)
