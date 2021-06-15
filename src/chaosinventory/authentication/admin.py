from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

# Register your models here.
from .models import Token, User
from .models.oidc import OIDCApplication


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


@admin.register(OIDCApplication)
class OIDCApplicationAdmin(admin.ModelAdmin):
    fields = (
        'client_id',
        'name',
        'description',
        'access_type',
        'default_redirect_uri',
        'redirect_uris',
        'created',
    )
    readonly_fields = (
        'client_id',
        'created',
    )
    list_display = (
        'name',
        'access_type',
        'created',
    )
    search_fields = (
        'client_id',
        'name',
        'description',
    )
    list_filter = (
        'access_type',
        'created',
    )

    def has_add_permission(self, request):
        """
        We do not want to create OIDCApplications from the admin interface.
        Use the create_oidc_application management command instead.
        """
        return False
