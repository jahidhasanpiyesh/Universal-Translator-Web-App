from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin

# 1. Age default User registration-ti bad dite hobe
admin.site.unregister(User)

# 2. Ekhon apnar custom admin class-ti likhun
@admin.register(User)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'first_name', 'is_staff', 'is_active')
    search_fields = ('username', 'email', 'first_name')
    ordering = ('username',)
    list_filter = ('is_staff', 'is_superuser', 'is_active')
    readonly_fields = ('date_joined', 'last_login')

    # Password field handle korar jonno fieldsets use kora hoy (Optional but good)