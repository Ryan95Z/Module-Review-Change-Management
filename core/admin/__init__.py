from django.contrib import admin
from django.contrib.auth.models import Group
from .year_tutor_admin import YearTutorAdmin
from .user_admin import UserAdmin
from .module_admin import ModuleAdmin
from core.models import *

admin.site.register(User, UserAdmin)
admin.site.unregister(Group)

admin.site.register(YearTutor, YearTutorAdmin)
admin.site.register(Module, ModuleAdmin)
