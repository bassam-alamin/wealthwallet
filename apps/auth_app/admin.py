from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from apps.auth_app.forms import UserChangeForm, UserCreationForm
from rangefilter.filters import DateRangeFilter
from django.utils import timezone
from .models import User


# Register your models here.
class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    readonly_fields = ('created_at', 'updated_at', 'password', 'created_by')
    form = UserChangeForm
    add_form = UserCreationForm
    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('email', 'full_name', 'admin', 'created_at',
                    'updated_at', 'created_by', 'days_since_last_login')
    list_filter = (("created_at", DateRangeFilter), 'created_by')
    date_hierarchy = 'created_at'
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {
            'fields': (
                'first_name', 'last_name',
                'username', 'email_verified', 'is_anonymous', "comments"
            )
        }),
        ('Permissions', {
            'fields': (
                'admin', 'staff', 'active',
                'groups', 'user_permissions'

            )
        }),
        ('Activity', {
            'fields': (
                'created_at', 'updated_at', 'last_login', "created_by"
            )
        })
    )

    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'email', 'first_name',
                'password1',
                'password2')}
         ),
    )
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()

    def full_name(self, obj):
        """Return the full name of the user in title case"""
        return f"{obj.first_name} {obj.last_name}".title()

    def days_since_last_login(self, obj):
        if obj.last_login:
            return (timezone.now() - obj.last_login).days
        return 0


admin.site.register(User, UserAdmin)