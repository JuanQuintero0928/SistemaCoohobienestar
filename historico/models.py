from django.db import models
from asociado.models import Asociado
from parametro.models import MesTarifa, FormaPago, TipoAuxilio
from beneficiario.models import Parentesco

# Create your models here.
class estadoOp(models.TextChoices):
    revision = 'REVISION', 'REVISION'
    otorgado = 'OTORGADO', 'OTORGADO'
    denegado = 'DENEGADO', 'DENEGADO'

class HistoricoAuxilio(models.Model):
    id = models.AutoField(primary_key=True)
    fechaSolicitud = models.DateField('Fecha Solicitud', blank=False, null=False)
    asociado = models.ForeignKey(Asociado, on_delete=models.RESTRICT, blank=False, null=False)
    tipoAuxilio = models.ForeignKey(TipoAuxilio, on_delete=models.RESTRICT, blank=False, null=False)
    valor = models.IntegerField('Valor', blank=False, null=False)
    estado = models.CharField('Estado', choices=estadoOp.choices, default=estadoOp.revision, blank=False, null=False)
    nombre = models.CharField('Nombre', max_length=70, blank=True, null=True)
    numDoc = models.CharField('Número Documento', max_length=11, blank=True, null=True)
    parentesco = models.ForeignKey(Parentesco, on_delete=models.RESTRICT, blank=True, null=True)
    nivelEducativo = models.CharField('Nivel Educativo', max_length=30, blank=True, null=True)
    anexoOne = models.CharField('Anexo 1', max_length=40, blank=True, null=True)
    anexoTwo = models.CharField('Anexo 2', max_length=40, blank=True, null=True)
    anexoThree = models.CharField('Anexo 3', max_length=40, blank=True, null=True)
    anexoFour = models.CharField('Anexo 4', max_length=40, blank=True, null=True)
    anexoFive = models.CharField('Anexo 5', max_length=40, blank=True, null=True)
    anexoSix = models.CharField('Anexo 6', max_length=40, blank=True, null=True)
    anexoSeven = models.CharField('Anexo 7', max_length=40, blank=True, null=True)
    anexoEight = models.CharField('Anexo 8', max_length=40, blank=True, null=True)
    fechaDesembolso = models.DateField('Fecha Desembolso', blank=True, null=True)
    estadoRegistro = models.BooleanField('Estado')
    fechaCreacion = models.DateTimeField(auto_now_add=True)
    fechaModificacion = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Historial de Auxilios'
        verbose_name_plural = 'Historial de Auxilios'
        ordering = ['pk']

    def __str__(self):
        return f"{self.id}"

class HistoricoCredito(models.Model):
    id = models.AutoField(primary_key=True)
    fechaSolicitud = models.DateField('Fecha Solicitud', blank=False, null=False)
    asociado = models.ForeignKey(Asociado, on_delete=models.RESTRICT, blank=False, null=False)
    valor = models.IntegerField('Valor', blank=False, null=False)
    cuotas = models.IntegerField('Cuotas', blank=False, null=False)
    estado = models.CharField('Estado', choices=estadoOp.choices, default=estadoOp.revision, blank=False, null=False)
    estadoRegistro = models.BooleanField('Estado')
    fechaCreacion = models.DateTimeField(auto_now_add=True)
    fechaModificacion = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Historial de Creditos'
        verbose_name_plural = 'Historial de Creditos'
        ordering = ['pk']

    def __str__(self):
        return f"{self.id}"

class HistorialPagos(models.Model):
    id = models.AutoField(primary_key=True)
    asociado = models.ForeignKey(Asociado, on_delete=models.RESTRICT, blank=False, null=False)
    mesPago = models.ForeignKey(MesTarifa, on_delete=models.RESTRICT, blank=False, null=False)
    valorPago = models.IntegerField('Valor Pago', blank=False, null=False)
    aportePago = models.IntegerField('Aporte', blank=False, null=False)
    bSocialPago = models.IntegerField('Bienestar Social', blank=False, null=False)
    mascotaPago = models.IntegerField('Mascota', blank=True, null=True)
    repatriacionPago = models.IntegerField('Repatriacion', blank=True, null=True)
    seguroVidaPago = models.IntegerField('Seguro Vida', blank=True, null=True)
    adicionalesPago = models.IntegerField('Adicionales', blank=True, null=True)
    coohopAporte = models.IntegerField('Coohoperativitos Aporte', blank=True, null=True)
    coohopBsocial = models.IntegerField('Coohoperativitos B Social', blank=True, null=True)
    diferencia = models.IntegerField('Diferencia', blank=True, null=True)
    formaPago = models.ForeignKey(FormaPago, on_delete=models.RESTRICT, blank=False, null=False)
    estadoRegistro = models.BooleanField('Estado')
    fechaCreacion = models.DateTimeField(auto_now_add=True)
    fechaModificacion = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Historial de Pagos'
        verbose_name_plural = 'Historial de Pagos'
        ordering = ['pk']
    
    def __str__(self):
        return f"{self.id}"
    
class HistoricoSeguroVida(models.Model):
    id = models.AutoField(primary_key=True)
    asociado = models.ForeignKey(Asociado, on_delete=models.RESTRICT, blank=False, null=False)
    valorPago = models.IntegerField('Valor Pago', blank=False, null=False)
    estadoRegistro = models.BooleanField('Estado')
    fechaIngreso = models.DateField('Fecha Ingreso', blank=False, null=False)
    fechaRetiro = models.DateField('Fecha Retiro', blank=True, null=True)
    fechaCreacion = models.DateTimeField(auto_now_add=True)
    fechaModificacion = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Seguro Vida'
        verbose_name_plural = 'Seguro Vida'
        ordering = ['pk']
    
    def __str__(self):
        return f"{self.id}"