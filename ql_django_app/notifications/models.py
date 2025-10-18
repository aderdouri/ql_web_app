from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Notification(models.Model):
    """Modèle pour les notifications du système d'administration"""
    
    NOTIFICATION_TYPES = [
        ('info', 'Information'),
        ('success', 'Success'),
        ('warning', 'Warning'),
        ('error', 'Error'),
        ('system', 'System'),
    ]
    
    PRIORITY_LEVELS = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('critical', 'Critical'),
    ]
    
    title = models.CharField(max_length=200, verbose_name="Title")
    message = models.TextField(verbose_name="Message")
    notification_type = models.CharField(
        max_length=20, 
        choices=NOTIFICATION_TYPES, 
        default='info',
        verbose_name="Type"
    )
    priority = models.CharField(
        max_length=20, 
        choices=PRIORITY_LEVELS, 
        default='medium',
        verbose_name="Priority"
    )
    is_read = models.BooleanField(default=False, verbose_name="Read")
    is_archived = models.BooleanField(default=False, verbose_name="Archived")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created At")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated At")
    expires_at = models.DateTimeField(null=True, blank=True, verbose_name="Expires At")
    
    # Relations
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True,
        verbose_name="User"
    )
    created_by = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='created_notifications',
        verbose_name="Created By"
    )
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = "Notification"
        verbose_name_plural = "Notifications"
    
    def __str__(self):
        return f"{self.title} - {self.get_notification_type_display()}"
    
    @property
    def is_expired(self):
        """Vérifie si la notification a expiré"""
        if self.expires_at:
            return timezone.now() > self.expires_at
        return False
    
    @property
    def time_ago(self):
        """Retourne le temps écoulé depuis la création"""
        delta = timezone.now() - self.created_at
        if delta.days > 0:
            return f"{delta.days} day{'s' if delta.days > 1 else ''} ago"
        elif delta.seconds > 3600:
            hours = delta.seconds // 3600
            return f"{hours} hour{'s' if hours > 1 else ''} ago"
        elif delta.seconds > 60:
            minutes = delta.seconds // 60
            return f"{minutes} minute{'s' if minutes > 1 else ''} ago"
        else:
            return "Just now"
    
    def mark_as_read(self):
        """Marque la notification comme lue"""
        self.is_read = True
        self.save()
    
    def mark_as_unread(self):
        """Marque la notification comme non lue"""
        self.is_read = False
        self.save()
    
    def archive(self):
        """Archive la notification"""
        self.is_archived = True
        self.save()
    
    def unarchive(self):
        """Désarchive la notification"""
        self.is_archived = False
        self.save()
