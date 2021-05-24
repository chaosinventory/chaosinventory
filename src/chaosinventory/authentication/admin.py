from django.contrib import admin

# Register your models here.
from .models import Token


@admin.register(Token)
class TokenAdmin(admin.ModelAdmin):
    fields = ('user',)
    list_display = ('id', 'key', 'user', 'created', 'application', 'expiring', 'renewable')
    actions = None
