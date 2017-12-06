from django.contrib import admin
from django.contrib.auth.models import Group

from .user_admin import UserCreationForm
from .user_admin import UserChangeForm
from .user_admin import UserAdmin
from core.models import User

admin.site.register(User, UserAdmin)
admin.site.unregister(Group)
