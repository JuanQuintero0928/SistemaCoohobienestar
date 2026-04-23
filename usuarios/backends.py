from django.core.cache import cache
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
import logging
import secrets

User = get_user_model()
logger = logging.getLogger('security')


class RateLimitExceeded(Exception):
    """Excepcion cuando se supera el limite de intentos"""
    pass


class RateLimitedAdminBackend(ModelBackend):
    """
    Rate limiting para login de admins (/accounts/login/)
    - 5 intentos fallidos maximos
    - 30 minutos de bloqueo
    - Bloquea por IP + username
    - Alerta cuando usuario valido intenta con contrasena incorrecta
    """
    minutes = 30
    requests = 5
    cache_prefix = 'ratelimit-admin-'
    
    def get_ip(self, request):
        """Obtiene la IP real del cliente"""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0].strip()
        else:
            ip = request.META.get('REMOTE_ADDR', '127.0.0.1')
        return ip
    
    def get_key(self, request, suffix):
        """Genera clave de cache"""
        ip = self.get_ip(request)
        return f'{self.cache_prefix}{ip}-{suffix}'
    
    def authenticate(self, request, username=None, password=None, **kwargs):
        if not username or not password:
            return None
        
        # Verificar si esta bloqueado por IP
        ip_key = self.get_key(request, 'ip')
        if cache.get(f'{ip_key}_blocked'):
            raise RateLimitExceeded('IP bloqueada. Demasiados intentos de login.')
        
        # Verificar bloqueo especifico por username
        username_key = self.get_key(request, f'user:{username}')
        if cache.get(f'{username_key}_blocked'):
            raise RateLimitExceeded('Usuario bloqueado temporalmente.')
        
        # Intentar autenticar
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            user = None
        
        if user is not None:
            # Verificar contrasena
            if user.check_password(password) and self.user_can_authenticate(user):
                # Login exitoso - limpiar intentos
                self._clear_attempts(request, username)
                return user
            else:
                # Usuario existe pero contrasena incorrecta - ES ALERTA DE SEGURIDAD
                self._handle_failed_attempt(request, username, is_valid_user=True)
                return None
        else:
            # Usuario no existe
            self._handle_failed_attempt(request, username, is_valid_user=False)
            return None
    
    def _handle_failed_attempt(self, request, username, is_valid_user):
        """Maneja intento fallido y genera alerta si es usuario valido"""
        ip = self.get_ip(request)
        
        # Incrementar contador por IP
        ip_key = self.get_key(request, 'ip')
        ip_attempts = cache.get(ip_key, 0) + 1
        cache.set(ip_key, ip_attempts, self.minutes * 60)
        
        # Incrementar contador por username
        username_key = self.get_key(request, f'user:{username}')
        username_attempts = cache.get(username_key, 0) + 1
        cache.set(username_key, username_attempts, self.minutes * 60)
        
        # Si es usuario valido, generar ALERTA
        if is_valid_user:
            self._send_security_alert(request, username, username_attempts)
        
        # Verificar si se alcanza el limite y bloquear - LANZAR EXCEPCION INMEDIATAMENTE
        if ip_attempts >= self.requests:
            # Bloquear IP
            cache.set(f'{ip_key}_blocked', True, self.minutes * 60)
            self._log_block(ip_address=ip, username=None, attempts=ip_attempts)
            logger.warning(f'IP {ip} bloqueada por {self.minutes} minutos tras {ip_attempts} intentos fallidos')
            raise RateLimitExceeded(f'IP bloqueada. Demasiados intentos de login. Intenta en {self.minutes} minutos.')
        
        if username_attempts >= self.requests:
            # Bloquear usuario
            cache.set(f'{username_key}_blocked', True, self.minutes * 60)
            self._log_block(ip_address=ip, username=username, attempts=username_attempts)
            logger.warning(f'Usuario {username} bloqueado por {self.minutes} minutos tras {username_attempts} intentos fallidos')
            raise RateLimitExceeded(f'Usuario {username} bloqueado temporalmente. Contacta al administrador.')
        
        # Registrar intento
        logger.info(f'Intento fallido: usuario={username}, IP={ip}, valido={is_valid_user}, intentos_ip={ip_attempts}, intentos_user={username_attempts}')
    
    def _send_security_alert(self, request, username, attempts):
        """Enviar alerta de seguridad cuando usuario valido intenta multiples veces"""
        ip = self.get_ip(request)
        
        # Alerta critica cuando usuario valido falla login
        if attempts >= 3:
            logger.critical(
                f'ALERTA SEGURIDAD: Usuario valido "{username}" tiene {attempts} '
                f'intentos fallidos desde IP {ip}. Posible intento de fuerza bruta.'
            )
    
    def _clear_attempts(self, request, username):
        """Limpia intentos al login exitoso"""
        ip = self.get_ip(request)
        cache.delete(self.get_key(request, 'ip'))
        cache.delete(self.get_key(request, f'user:{username}'))
        logger.info(f'Login exitoso: usuario={username}, IP={ip}. Intentos previos limpiados.')
    
    def _log_block(self, ip_address, username, attempts):
        """Registra bloqueo en BD para auditoria"""
        try:
            from usuarios.models import LoginBlockLog
            from datetime import timedelta
            
            unlock_token = secrets.token_urlsafe(32)
            blocked_until = timezone.now() + timedelta(minutes=self.minutes)
            
            LoginBlockLog.objects.create(
                ip_address=ip_address,
                username=username,
                blocked_until=blocked_until,
                reason='rate_limit',
                unlock_token=unlock_token,
                attempts_count=attempts
            )
        except Exception as e:
            logger.error(f'Error al registrar bloqueo: {e}')
