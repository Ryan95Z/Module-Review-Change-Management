from django.contrib import admin
from timeline.models import TableChange


class TableChangesAdmin(admin.ModelAdmin):
    list_display = ('changes_for_model', 'changes_field', 'current_value', 'new_value',
                    'related_entry', 'model_id')

admin.site.register(TableChange, TableChangesAdmin)
