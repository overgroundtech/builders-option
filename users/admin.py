from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group

admin.site.unregister(get_user_model())
admin.site.unregister(Group)


@admin.register(get_user_model())
class CustomUserAdmin(UserAdmin):
    def has_change_permission(self, request, obj=None):
        return False



