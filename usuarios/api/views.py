from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.contrib.auth.hashers import make_password
from django.utils.timezone import now
from django.conf import settings
from django.core.mail import send_mail
from usuarios.utils import generar_y_enviar_codigo_otp

from usuarios.serializers import RegistroAsociadoSerializer
from usuarios.models import UsuarioAsociado


class RegistroAsociadoView(APIView):
    def post(self, request):
        serializer = RegistroAsociadoSerializer(data=request.data)
        if serializer.is_valid():
            usuario = serializer.save()
            return Response(
                {
                    "message": "Cuenta creada exitosamente.",
                    "redirect_url": f"/accounts/verificacionCuenta/?email={usuario.email}"
                }, 
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class VerificarCodigoView(APIView):
    def post(self, request):
        email = request.data.get("email")
        codigo = request.data.get("codigo")

        if not email or not codigo:
            return Response({"error": "Email y código son obligatorios."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            usuario = UsuarioAsociado.objects.get(email=email, verification_code=codigo)

            if usuario.verification_expires < now():
                return Response({"error": "El código de verificación ha expirado."}, status=status.HTTP_400_BAD_REQUEST)

            usuario.is_active = True
            usuario.verification_code = None
            usuario.save()

            return Response({"message": "Cuenta activada exitosamente."}, status=status.HTTP_200_OK)

        except UsuarioAsociado.DoesNotExist:
            return Response({"error": "Código inválido o usuario no encontrado."}, status=status.HTTP_400_BAD_REQUEST)


class ReenviarCodigoView(APIView):
    def post(self, request):
        email = request.data.get('email', '').lower()

        try:
            usuario = UsuarioAsociado.objects.get(username=email, is_associate=True, is_active=False)
        except UsuarioAsociado.DoesNotExist:
            return Response({'error': 'No se encontró una cuenta pendiente de activación con este correo.'},
                            status=status.HTTP_400_BAD_REQUEST)

        # Llamas la función sin pasar el código explícitamente
        generar_y_enviar_codigo_otp(usuario, codigo=None)

        return Response({'message': 'Código reenviado correctamente.'}, status=status.HTTP_200_OK)
