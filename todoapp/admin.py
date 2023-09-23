from django.contrib import admin
from .models import User, Task
from .forms import CustomUserChangeForm, CustomUserCreationForm
from django.contrib.auth.admin import UserAdmin

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = User
    list_display = ['username', 'full_name', 'is_active', 'last_login']
    readonly_fields = ["date_joined"]
    fieldsets = [
        (
            None,
            {
                'fields': ['username', 'full_name', 'last_login', 'date_joined'],
            },
        ),
        (
            'Advanced options',
            {
                'classes': ['collapse'],
                'fields': ['password', 'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'],
            },
        ),
    ]
    add_fieldsets = [
        (
            None,
            {
                'fields': ['username', 'full_name', 'password1', 'password2'],
            },
        ),
        (
            'Advanced options',
            {
                'classes': ['collapse'],

                'fields': ['is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'],
            },
        ),
    ]

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ['title', 'description', 'due_date', 'completed']
