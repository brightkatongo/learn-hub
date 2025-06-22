from django.contrib import admin
from .models import Notification, NotificationPreference, Announcement

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('title', 'recipient', 'notification_type', 'is_read', 'created_at')
    list_filter = ('notification_type', 'is_read', 'created_at')
    search_fields = ('title', 'recipient__email', 'message')
    readonly_fields = ('id', 'created_at')

@admin.register(NotificationPreference)
class NotificationPreferenceAdmin(admin.ModelAdmin):
    list_display = ('user', 'email_notifications', 'push_notifications', 'course_updates')
    search_fields = ('user__email',)

@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ('title', 'announcement_type', 'priority', 'is_active', 'start_date', 'end_date')
    list_filter = ('announcement_type', 'priority', 'is_active', 'start_date')
    search_fields = ('title', 'content')
    filter_horizontal = ('target_users',)
