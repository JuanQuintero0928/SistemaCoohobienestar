from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from django.conf import settings
from asociado.models import Asociado

class UsuarioAsociado(AbstractUser):
    is_associate = models.BooleanField(default=False)
    asociado = models.OneToOneField(Asociado, on_delete=models.CASCADE, null=True, blank=True)
    verification_code = models.CharField(max_length=6, blank=True, null=True)
    verification_expires = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.username


class LoginBlockLog(models.Model):
    """Log de bloqueos por rate limiting - para auditoria y desbloqueo manual"""
    REASON_CHOICES = [
        ('rate_limit', 'Rate Limit'),
        ('manual', 'Desbloqueo Manual'),
    ]
    
    ip_address = models.GenericIPAddressField()
    username = models.CharField(max_length=150, null=True, blank=True)
    blocked_at = models.DateTimeField(auto_now_add=True)
    blocked_until = models.DateTimeField()
    reason = models.CharField(max_length=50, default='rate_limit')
    unlock_token = models.CharField(max_length=64, unique=True, blank=True)
    attempts_count = models.IntegerField(default=0)
    unlocked_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        null=True, 
        blank=True, 
        on_delete=models.SET_NULL,
        related_name='unlocked_logins'
    )
    unlocked_at = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['-blocked_at']
        verbose_name = 'Bloqueo de Login'
        verbose_name_plural = 'Bloqueos de Login'
    
    def __str__(self):
        return f"{self.username or self.ip_address} - {self.blocked_at}"
    
    def save(self, *args, **kwargs):
        if not self.unlock_token:
            import secrets
            self.unlock_token = secrets.token_urlsafe(32)
        super().save(*args, **kwargs)
    
    @property
    def is_expired(self):
        return timezone.now() > self.blocked_until
    
    @property
    def remaining_minutes(self):
        diff = self.blocked_until - timezone.now()
        return max(0, int(diff.total_seconds() / 60))