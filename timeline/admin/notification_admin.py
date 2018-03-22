from django.contrib import admin
from timeline.models import Notification


class NotificationAdmin(admin.ModelAdmin):
    list_display = ('content', 'seen')

admin.site.register(Notification, NotificationAdmin)
