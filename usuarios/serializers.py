from rest_framework import serializers
from django.core.mail import send_mail
from django.utils.crypto import get_random_string
from django.utils.timezone import now, timedelta
from django.conf import settings
from rest_framework import status
from rest_framework.response import Response

from usuarios.models import UsuarioAsociado
from asociado.models import Asociado

class RegistroAsociadoSerializer(serializers.Serializer):
    cedula = serializers.CharField()
    fecha_expedicion = serializers.DateField()
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        
        # Validar si el email ya tiene una cuenta asociada
        if UsuarioAsociado.objects.filter(username=data['email']).exists():
            raise serializers.ValidationError({"email": "El email ya tiene una cuenta asociada."})

        try :
             # Validar si la cedula y fecha de expedicion son correctas con la informacion de la db
            asociado = Asociado.objects.get(numDocumento = data['cedula'], fechaExpedicion = data['fecha_expedicion'])
        except Asociado.DoesNotExist:
            raise serializers.ValidationError([
                                                "Los datos no coinciden con ningún asociado registrado.",
                                                "Verifique:",
                                                "• Número de documento",
                                                "• Fecha de expedición",
                                                "O contacte a Coohobienestar."
                                            ])

        if UsuarioAsociado.objects.filter(asociado=asociado).exists():
            raise serializers.ValidationError("El asociado ya tiene una cuenta asociada.")
        
        data['asociado'] = asociado
        return data
    
    def create(self, validated_data):
      
        """Generar código de verificación y enviarlo por correo"""
        asociado = validated_data.pop('asociado')
        password = validated_data.pop('password')
        email = (validated_data.get("email")).lower()
        
        # Generar código único de 6 dígitos
        codigo_verificacion = get_random_string(length=6, allowed_chars='0123456789')
        
        usuario = UsuarioAsociado.objects.create(
            username=email,
            email=email,
            password=password,  # No se encripta aún hasta la activación
            is_active=False,  # Se activa cuando ingrese el código
            is_associate=True,
            asociado=asociado,
            verification_code=codigo_verificacion,  # Guarda el código en la BD
            verification_expires=now() + timedelta(minutes=10)  # Expira en 10 min
        )

        # Enviar el código por correo
        send_mail(
            "Código de verificación - Coohobienestar",
            f"Tu código de verificación es: {codigo_verificacion}\nEste código expira en 10 minutos.",
            settings.DEFAULT_FROM_EMAIL,  # Usa la configuración del .env
            [usuario.email],
            fail_silently=False,
        )

        return usuario