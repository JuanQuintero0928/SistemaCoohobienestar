from django.db import models
from departamento.models import PaisRepatriacion 
from asociado.models import Asociado

# Create your models here.

class Parentesco(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField('Nombre', max_length=30, null=False, blank=False)

    class Meta:
        verbose_name = 'Parentesco'
        ordering = ['nombre']
    
    def __str__(self):
        return self.nombre

class tipoDocumentoOp(models.TextChoices):
    cedula = 'CEDULA', 'Cedula' 
    registroCivil = 'REGISTRO CIVIL', 'Registro Civil'
    tarjetaIdentidad = 'TARJETA IDENTIDAD', 'Tarjeta Identidad'
    cedulaExtranjera = 'CEDULA EXTRANJERA', 'Cedula Extranjera'
    pasaporte = 'PASAPORTE', 'Pasaporte'
    ppt = 'PPT', 'PPT'

class Beneficiario(models.Model):
    id = models.AutoField(primary_key=True)
    asociado = models.ForeignKey(Asociado, on_delete=models.RESTRICT, blank=False, null=False)
    nombre = models.CharField('Nombre', max_length=50, null=False, blank=False)
    apellido = models.CharField('Apellido', max_length=50, null=False, blank=False)
    tipoDocumento = models.CharField('Tipo Documento', choices=tipoDocumentoOp.choices, default=tipoDocumentoOp.cedula, blank=False, null=False)
    numDocumento = models.CharField('Número Documento', max_length=12, blank=False, null=False)
    fechaNacimiento = models.DateField('Fecha Nacimiento', blank=False, null=False)
    parentesco = models.ForeignKey(Parentesco, on_delete=models.RESTRICT, blank=False, null=False)
    repatriacion = models.BooleanField('Repatriacion')
    paisRepatriacion = models.ForeignKey(PaisRepatriacion, on_delete=models.RESTRICT, blank=True, null=True)
    fechaRepatriacion = models.DateField('Fecha Repatriacion', blank=True, null=True)
    ciudadRepatriacion = models.CharField('Ciudad Repatriación', max_length=50, blank=True, null=True)
    estadoRegistro = models.BooleanField('Estado')
    fechaIngreso = models.DateField('Fecha Ingreso', blank=False, null=False)
    fechaRetiro = models.DateField('Fecha Retiro', blank=True, null=True)
    fechaCreacion = models.DateTimeField(auto_now_add=True)
    fechaModificacion = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Beneficiario'
        ordering = ['pk']
    
    def __str__(self):
        return self.nombre
    
class Mascota(models.Model):

    class tipoOp(models.TextChoices):
        perro = 'PERRO', 'Perro'
        gato = 'GATO', 'Gato'

    id = models.AutoField(primary_key=True)
    asociado = models.ForeignKey(Asociado, on_delete=models.RESTRICT, blank=False, null=False)
    nombre = models.CharField('Nombre', max_length=30, null=False, blank=False)
    tipo = models.CharField('Tipo', choices=tipoOp.choices, default=tipoOp.perro, max_length=30, null=False, blank=False)
    raza = models.CharField('Raza', max_length=30, null=False, blank=False)
    fechaNacimiento = models.DateField('Fecha Nacimiento', blank=False, null=False)
    vacunasCompletas = models.BooleanField('Vacunas Completas')
    estadoRegistro = models.BooleanField('Estado')
    fechaIngreso = models.DateField('Fecha Ingreso', blank=False, null=False)
    fechaRetiro = models.DateField('Fecha Retiro', blank=True, null=True)
    fechaCreacion = models.DateTimeField(auto_now_add=True)
    fechaModificacion = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Mascota'
        ordering = ['pk']
    
    def __str__(self):
        return self.nombre
    
class Coohoperativitos(models.Model):
    id = models.AutoField(primary_key=True)
    asociado = models.ForeignKey(Asociado, on_delete=models.RESTRICT, blank=False, null=False)
    nombre = models.CharField('Nombre', max_length=30, null=False, blank=False)
    apellido = models.CharField('Apellido', max_length=30, null=False, blank=False)
    tipoDocumento = models.CharField('Tipo Documento', choices=tipoDocumentoOp.choices, default=tipoDocumentoOp.cedula, blank=False, null=False)
    numDocumento = models.CharField('Número Documento', max_length=10, blank=False, null=False)
    estadoRegistro = models.BooleanField('Estado')
    fechaNacimiento = models.DateField('Fecha Nacimiento', blank=True, null=True)
    fechaIngreso = models.DateField('Fecha Ingreso', blank=False, null=False)
    fechaRetiro = models.DateField('Fecha Retiro', blank=True, null=True)
    fechaCreacion = models.DateTimeField(auto_now_add=True)
    fechaModificacion = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Coohoperativitos'
        verbose_name_plural = 'Coohoperativitos'
        ordering = ['pk']
    
    def __str__(self):
        return self.nombre