from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

# Register your models here.
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('email', 'is_staff', 'is_active', 'is_superuser', 'is_verified')
    list_filter = ('is_staff', 'is_active', 'is_superuser', 'is_verified')
    search_fields = ('email',)
    ordering = ('email',)
    
    fieldsets = (
        ('Authentication', {
            "fields": (
                'email','password',
            ),
        }),
        ('Permissions', {
            "fields": (
                'is_staff','is_active','is_superuser','is_verified',
            ),
        }),
        
        ('group permissions', {
            "fields": (
                'groups','user_permissions'
            ),
        }),
        
        ('Important date', {
            "fields": (
                'last_login',
            ),
        }),
    )
    
    add_fieldsets = [
        (
            None,
            {
                "classes": ["wide"],
                "fields": ["email", "password1", "password2","is_staff", "is_active", 'is_superuser','is_verified'],
            },
        ),
    ]

admin.site.register(CustomUser, CustomUserAdmin)