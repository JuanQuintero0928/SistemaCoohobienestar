from django.db import models
from departamento.models import Departamento, Municipio
from historico.models import HistoricoCredito
from asociado.models import generoOp, estadoCivilOp, tipoDocumentoOp, tipoViviendaOp, Asociado

# Create your models here.

class Codeudor(models.Model):
    id = models.AutoField(primary_key=True)
    asociado = models.ForeignKey(Asociado, on_delete=models.RESTRICT, blank=False, null=False)
    historicoCredito = models.ForeignKey(HistoricoCredito, on_delete=models.RESTRICT, blank=False, null=False)
    nombre = models.CharField(max_length=30, null=False, blank=False)
    apellido = models.CharField(max_length=30, null=False, blank=False)
    tipoDocumento = models.CharField(choices=tipoDocumentoOp.choices, default=tipoDocumentoOp.cedula, blank=False, null=False)
    numDocumento = models.CharField(max_length=11, blank=False, null=False)
    fechaExpedicion = models.DateField(blank=False, null=False)
    mpioDoc = models.ForeignKey(Municipio, on_delete=models.RESTRICT, blank=False, null=False)
    nacionalidad = models.CharField(max_length=30, null=False, blank=False)
    genero = models.CharField(choices=generoOp.choices, default=generoOp.masculino, blank=False, null=False)
    estadoCivil = models.CharField(choices=estadoCivilOp.choices, default=estadoCivilOp.soltero, blank=False, null=False)
    email = models.EmailField(blank=False, null=False)
    fechaNacimiento = models.DateField(blank=False, null=False)
    dtoNacimiento = models.ForeignKey(Departamento, on_delete=models.RESTRICT, blank=False, null=False, related_name='dtoNacimientoCod')
    mpioNacimiento = models.ForeignKey(Municipio, on_delete=models.RESTRICT, blank=False, null=False, related_name='mpioNacimientoCod')
    tipoVivienda = models.CharField(choices=tipoViviendaOp.choices, default=tipoViviendaOp.propia, blank=True, null=True)
    estrato = models.IntegerField(blank=False, null=False)
    direccion = models.CharField(max_length=50, blank=False, null=False)
    barrio = models.CharField(max_length=50, blank=False, null=False)
    deptoResidencia = models.ForeignKey(Departamento, on_delete=models.RESTRICT, blank=False, null=False, related_name='deptoResidenciaCod')
    mpioResidencia = models.ForeignKey(Municipio, on_delete=models.RESTRICT, blank=False, null=False, related_name='mpioResidenciaCod')
    numCelular = models.CharField(max_length=13, blank=False, null=False)
    ingresosTotales = models.IntegerField(blank=False, null=False)
    egresosTotales = models.IntegerField(blank=False, null=False)
    estadoRegistro = models.BooleanField(default=True)
    fechaCreacion = models.DateTimeField(auto_now_add=True)
    fechaModificacion = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.nombre} {self.apellido}"