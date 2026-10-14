"""Use Django's account tools without allowing support staff to grant privileges."""
from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

User = get_user_model()
admin.site.unregister(User)


@admin.register(User)
class HuntItUserAdmin(UserAdmin):
    def get_readonly_fields(self, request, obj=None):
        fields = list(super().get_readonly_fields(request, obj))
        if not request.user.is_superuser:
            fields.extend(["is_staff", "is_superuser", "groups", "user_permissions"])
        return fields

    def has_add_permission(self, request):
        return request.user.is_superuser and super().has_add_permission(request)

    def has_change_permission(self, request, obj=None):
        if obj and not request.user.is_superuser and (obj.is_staff or obj.is_superuser) and obj.pk != request.user.pk:
            return False
        return super().has_change_permission(request, obj)

    def has_delete_permission(self, request, obj=None):
        if obj and (obj.pk == request.user.pk or (not request.user.is_superuser and (obj.is_staff or obj.is_superuser))):
            return False
        return super().has_delete_permission(request, obj)
