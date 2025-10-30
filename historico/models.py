from django.db import models
from django.conf import settings
from asociado.models import Asociado, ConvenioHistoricoGasolina
from parametro.models import MesTarifa, FormaPago, TipoAuxilio, TasasInteresCredito
from beneficiario.models import Parentesco

# Create your models here.
class estadoOp(models.TextChoices):
    revision = 'REVISION', 'REVISION'
    otorgado = 'OTORGADO', 'OTORGADO'
    denegado = 'DENEGADO', 'DENEGADO'

class lineaCreditoOp(models.TextChoices):
    anticipoNomina = 'ANTICIPO NOMINA', 'ANTICIPO NOMINA'
    solucionInmediata = 'SOLUCION INMEDIATA', 'SOLUCION INMEDIATA'
    crediLibre = 'CREDILIBRE', 'CREDILIBRE'
    crediContigo = 'CREDICONTIGO', 'CREDICONTIGO'
    kupi = 'KUPI', 'KUPI'
    crediSeguro = 'CREDISEGURO', 'CREDISEGURO'
    creditoSoat = 'CREDITO SOAT', 'CREDITO SOAT'

class amortizacionOP(models.TextChoices):
    cuotaFija = 'CUOTA FIJA', 'CUOTA FIJA'
    cuotaVariable = 'CUOTA VARIABLE', 'CUOTA VARIABLE'

class mediodePagoOp(models.TextChoices):
    pagoDirecto = 'PAGO DIRECTO', 'PAGO DIRECTO'
    nomina = 'NOMINA', 'NOMINA'
    libranza = 'LIBRANZA', 'LIBRANZA'

class formaDesembolsoOp(models.TextChoices):
    transferenciaElectronica = 'TRANSFERENCIA ELECTRONICA', 'TRANSFERENCIA ELECTRONICA'
    cheque = 'CHEQUE', 'CHEQUE'
    cuentaAhorros = 'CUENTA AHORROS', 'CUENTA AHORROS'

class HistoricoAuxilio(models.Model):
    id = models.AutoField(primary_key=True)
    fechaSolicitud = models.DateField('Fecha Solicitud', blank=False, null=False)
    asociado = models.ForeignKey(Asociado, on_delete=models.RESTRICT, blank=False, null=False)
    tipoAuxilio = models.ForeignKey(TipoAuxilio, on_delete=models.RESTRICT, blank=False, null=False)
    entidadBancaria = models.CharField('Entidad Bancaria', max_length=30, blank=True, null=True)
    numCuenta = models.CharField('Número Cuenta', max_length=30, blank=True, null=True)
    valor = models.IntegerField('Valor', blank=False, null=False)
    estado = models.CharField('Estado', choices=estadoOp.choices, default=estadoOp.revision, blank=False, null=False)
    nombre = models.CharField('Nombre', max_length=70, blank=True, null=True)
    numDoc = models.CharField('Número Documento', max_length=11, blank=True, null=True)
    parentesco = models.ForeignKey(Parentesco, on_delete=models.RESTRICT, blank=True, null=True)
    nivelEducativo = models.CharField('Nivel Educativo', max_length=100, blank=True, null=True)
    anexoOne = models.CharField('Anexo 1', max_length=40, blank=True, null=True)
    anexoTwo = models.CharField('Anexo 2', max_length=40, blank=True, null=True)
    anexoThree = models.CharField('Anexo 3', max_length=40, blank=True, null=True)
    anexoFour = models.CharField('Anexo 4', max_length=40, blank=True, null=True)
    anexoFive = models.CharField('Anexo 5', max_length=40, blank=True, null=True)
    anexoSix = models.CharField('Anexo 6', max_length=40, blank=True, null=True)
    anexoSeven = models.CharField('Anexo 7', max_length=40, blank=True, null=True)
    anexoEight = models.CharField('Anexo 8', max_length=40, blank=True, null=True)
    observacion = models.CharField('Observaciones', max_length=200, blank=True, null=True)
    motivoEliminacion = models.CharField('Motivo de Eliminacion', max_length=200, blank=True, null=True)
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
    
    @property
    def anexos(self):
        return f"{self.anexoOne}, {self.anexoTwo}, {self.anexoThree}, {self.anexoFour}, {self.anexoFive}, {self.anexoSix}, {self.anexoSeven}, {self.anexoEight}"


class TipoCuentaOp(models.TextChoices):
        ahorros = 'CUENTA AHORROS', 'CUENTA AHORROS'
        corriente = 'CUENTA CORRIENTE', 'CUENTA CORRIENTE'

class HistoricoCredito(models.Model):
    id = models.AutoField(primary_key=True)
    fechaSolicitud = models.DateField('Fecha Solicitud', blank=False, null=False)
    asociado = models.ForeignKey(Asociado, on_delete=models.RESTRICT, blank=False, null=False)
    valor = models.IntegerField('Valor', blank=False, null=False)
    lineaCredito = models.CharField('Linea Credito', choices=lineaCreditoOp.choices, default=lineaCreditoOp.solucionInmediata, blank=False, null=False)
    amortizacion = models.CharField('Amortización', choices=amortizacionOP.choices, default=amortizacionOP.cuotaFija, blank=False, null=False)
    tasaInteres = models.ForeignKey(TasasInteresCredito, on_delete=models.RESTRICT, blank=True, null=True)
    cuotas = models.IntegerField('Cuotas', blank=False, null=False)
    valorCuota = models.IntegerField('Valor Cuota', blank=False, null=False)
    totalCredito = models.IntegerField('Total Credito', blank=False, null=False)
    medioPago = models.CharField('Medio de Pago', choices=mediodePagoOp.choices, default=mediodePagoOp.pagoDirecto, blank=False, null=False)
    formaDesembolso = models.CharField('Forma de Desembolso', choices=formaDesembolsoOp.choices, default=formaDesembolsoOp.transferenciaElectronica, blank=False, null=False)
    estado = models.CharField('Estado', choices=estadoOp.choices, default=estadoOp.revision, blank=False, null=False)
    banco = models.CharField('Banco', max_length=30, blank=True, null=True)
    numCuenta = models.CharField('Numero Cuenta', max_length=30, blank=True, null=True)
    tipoCuenta = models.CharField('Tipo Cuenta', choices=TipoCuentaOp.choices, blank=True, null=True)
    cuotasPagas = models.IntegerField(blank=True, null=True)
    pendientePago = models.IntegerField(blank=True, null=True)
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
    fechaPago = models.DateField('Fecha Pago', blank=True, null=True)
    valorPago = models.IntegerField('Valor Pago', blank=False, null=False)
    aportePago = models.IntegerField('Aporte', blank=False, null=False)
    bSocialPago = models.IntegerField('Bienestar Social', blank=False, null=False)
    mascotaPago = models.IntegerField('Mascota', blank=True, null=True)
    repatriacionPago = models.IntegerField('Repatriacion', blank=True, null=True)
    seguroVidaPago = models.IntegerField('Seguro Vida', blank=True, null=True)
    adicionalesPago = models.IntegerField('Adicionales', blank=True, null=True)
    coohopAporte = models.IntegerField('Coohoperativitos Aporte', blank=True, null=True)
    coohopBsocial = models.IntegerField('Coohoperativitos B Social', blank=True, null=True)
    convenioPago = models.IntegerField('Convenio', blank=True, null=True)
    creditoHomeElements = models.IntegerField('Credito Home Elements', blank=True, null=True)
    credito = models.IntegerField('Credito', blank=True, null=True)
    diferencia = models.IntegerField('Diferencia', blank=True, null=True)
    formaPago = models.ForeignKey(FormaPago, on_delete=models.RESTRICT, blank=False, null=False)
    ventaHE = models.ForeignKey('ventas.HistoricoVenta', on_delete=models.CASCADE, related_name='pagosHE', blank=True, null=True)
    creditoId = models.ForeignKey('HistoricoCredito', on_delete=models.CASCADE, related_name='pagosCredito', blank=True, null=True)
    convenio_gasolina_id = models.ForeignKey(ConvenioHistoricoGasolina, on_delete=models.CASCADE, related_name='pagosGasolina', blank=True, null=True)
    userCreacion = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='usuario_creacion', on_delete=models.CASCADE, blank=True, null=True)
    userModificacion = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='usuario_modificacion', on_delete=models.CASCADE, blank=True, null=True)
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
    primerMesSeguroVida = models.ForeignKey(
        MesTarifa,
        on_delete=models.RESTRICT,
        blank=True,
        null=True,
        related_name='historico_seguro_vida'
    )
    fechaRetiro = models.DateField('Fecha Retiro', blank=True, null=True)
    fechaCreacion = models.DateTimeField(auto_now_add=True)
    fechaModificacion = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Seguro Vida'
        verbose_name_plural = 'Seguro Vida'
        ordering = ['pk']
    
    def __str__(self):
        return f"{self.id}"