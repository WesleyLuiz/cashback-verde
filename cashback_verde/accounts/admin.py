from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from .models import User


@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    list_display = ('username', 'email', 'role', 'cashback_balance', 'is_staff', 'is_active')
    list_filter = ('role', 'is_staff', 'is_superuser', 'is_active', 'groups')
    fieldsets = DjangoUserAdmin.fieldsets + (
        ('Perfil no marketplace', {'fields': ('role', 'cashback_balance')}),
    )
    add_fieldsets = DjangoUserAdmin.add_fieldsets + (
        ('Perfil no marketplace', {'fields': ('email', 'role')}),
    )
