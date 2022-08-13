from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import CustomUser
# Register your models here.

class CustomUserAdmin(UserAdmin):
    ordering = ("username",)
    list_display = ( "username", "email", "is_active")
    search_fields=['username',"first_name", "email","last_name"]
    list_filter = ['date_joined','is_active','is_staff','is_superuser']
    

    fieldsets= (
        ("Personal Info", {
            "fields": ('username','email', 'password',)
        }),

        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')
        }),

        ('Important Dates', {
            'fields': ('date_joined', 'last_login')
        })
    )

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ('username', "password1", "password2"),
            },
            
        ),
           (
            'More info',
            {
                "fields": ('email', 'first_name', 'last_name',),
            },
            
        ),
        (
            'Permissions', 
            {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')
            }
        ),
    )


    readonly_fields= ['date_joined', 'last_login']


admin.site.register(CustomUser, CustomUserAdmin)

