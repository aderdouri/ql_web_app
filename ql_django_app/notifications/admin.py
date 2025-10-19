from django.contrib import admin
from .models import Notification

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ['title', 'notification_type', 'priority', 'is_read', 'user', 'created_at']
    list_filter = ['notification_type', 'priority', 'is_read', 'is_archived', 'created_at']
    search_fields = ['title', 'message', 'user__username']
    readonly_fields = ['created_at', 'updated_at']
    ordering = ['-created_at']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'message', 'notification_type', 'priority')
        }),
        ('Status', {
            'fields': ('is_read', 'is_archived')
        }),
        ('Relations', {
            'fields': ('user', 'created_by')
        }),
        ('Timing', {
            'fields': ('created_at', 'updated_at', 'expires_at')
        }),
    )

