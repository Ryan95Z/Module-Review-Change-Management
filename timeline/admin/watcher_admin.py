from django.contrib import admin
from timeline.models import Watcher


class WatcherAdmin(admin.ModelAdmin):
    list_display = ('pk', )


admin.site.register(Watcher, WatcherAdmin)
