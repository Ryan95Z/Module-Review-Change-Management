from django.contrib import admin


class ModuleAdmin(admin.ModelAdmin):
    list_display = ('module_code', 'module_name',
                    'module_credits', 'module_leader_name')

    search_fields = ('module_code', 'module_name')

    ordering = ('module_code', )

    def module_leader_name(self, obj):
        return obj.module_leader_name()
