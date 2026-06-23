from django.contrib import admin
from .models import Profile
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin

class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    fields = ('is_moderator', 'is_blocked', 'blocked_until', 'bio', 'avatar')

class CustomUserAdmin(UserAdmin):
    inlines = [ProfileInline]
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'is_moderator', 'is_blocked')

    def is_moderator(self, obj):
        if hasattr(obj, 'profile'):
            return obj.profile.is_moderator
        return False

    is_moderator.boolean = True
    is_moderator.short_description = 'Moderator'

    def is_blocked(self, obj):
        if hasattr(obj, 'profile'):
            return obj.profile.is_blocked
        return False

    is_blocked.boolean = True
    is_blocked.short_description = 'Blocked'

admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)