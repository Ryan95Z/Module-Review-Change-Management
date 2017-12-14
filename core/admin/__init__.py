from django.contrib import admin
from django.contrib.auth.models import Group
from .year_tutor_admin import YearTutorAdmin
from .user_admin import UserAdmin
from core.models import User, YearTutor

admin.site.register(User, UserAdmin)
admin.site.unregister(Group)

admin.site.register(YearTutor, YearTutorAdmin)
