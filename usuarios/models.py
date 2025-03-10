from django.contrib.auth.models import AbstractUser
from django.db import models
from asociado.models import Asociado

class UsuarioAsociado(AbstractUser):
    is_associate = models.BooleanField(default=False)
    asociado = models.OneToOneField(Asociado, on_delete=models.CASCADE, null=True, blank=True)
    verification_code = models.CharField(max_length=6, blank=True, null=True)
    verification_expires = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.username