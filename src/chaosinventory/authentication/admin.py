from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

# Register your models here.
from .models import Token, User


@admin.register(User)
class UserAdmin(UserAdmin):
    readonly_fields = ('uuid',)
    fieldsets = (
        (None, {'fields': ('uuid', 'username', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email')}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )


@admin.register(Token)
class TokenAdmin(admin.ModelAdmin):
    fields = ('user',)
    list_display = ('id', 'key', 'user', 'created', 'application', 'expiring', 'renewable')
    actions = None
