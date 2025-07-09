# usuarios/utils.py
from django.core.mail import send_mail
from django.conf import settings
from django.utils.crypto import get_random_string
from django.utils.timezone import now, timedelta

def generar_y_enviar_codigo_otp(usuario, codigo):
    if codigo is None:
        codigo = get_random_string(length=6, allowed_chars='0123456789')
        usuario.verification_code = codigo
        usuario.verification_expires = now() + timedelta(minutes=10)
        usuario.save()

    asunto = "Código de verificación - Coohobienestar"
    mensaje = f"""
Hola {usuario.asociado.nombre} {usuario.asociado.apellido},

Recibiste este mensaje porque estás creando una cuenta en Coohobienestar.

Tu código de verificación es:

    {codigo}

Este código es válido por 10 minutos. Por favor, no lo compartas con nadie.

Si no solicitaste este código, puedes ignorar este mensaje.

Saludos cordiales,  
Equipo de Coohobienestar
    """.strip()

    send_mail(
        asunto,
        mensaje,
        settings.DEFAULT_FROM_EMAIL,
        [usuario.email],
        fail_silently=False,
    )
