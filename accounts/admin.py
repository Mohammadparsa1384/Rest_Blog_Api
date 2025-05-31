from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Profile

admin.site.site_title = "Rest blog admin panel"
admin.site.site_header = "Rest blog admin panel"
admin.site.site_title = "Rest blog admin panel"
admin.site.index_title = "Admin panel"

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

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'first_name', 'last_name', 'created_date')
    search_fields = ('user__email', 'first_name', 'last_name')