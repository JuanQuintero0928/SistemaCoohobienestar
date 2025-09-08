from django.db import models
from departamento.models import Departamento, Municipio, PaisRepatriacion, Pais
from parametro.models import FormaPago, TipoAsociado, ServicioFuneraria, MesTarifa, Convenio
# from historico.models import HistoricoCredito

# Create your models here.

class tipoPersonaOp(models.TextChoices):
        pNatural = 'PERSONA NATURAL', 'PERSONA NATURAL'
        pjuridica = 'PERSONA JURIDICA', 'PERSONA JURIDICA'

class tipoDocumentoOp(models.TextChoices):
    cedula = 'CEDULA', 'CEDULA' 
    registroCivil = 'REGISTRO CIVIL', 'REGISTRO CIVIL'
    tarjetaIdentidad = 'TARJETA IDENTIDAD', 'TARJETA IDENTIDAD'
    cedulaExtranjera = 'CEDULA EXTRANJERA', 'CEDULA EXTRANJERA'
    pasaporte = 'PASAPORTE', 'PASAPORTE'
    ppt = 'PPT', 'PPT'

class generoOp(models.TextChoices):
    masculino = 'MASCULINO', 'MASCULINO'
    femenino = 'FEMENINO', 'FEMENINO'

class estadoCivilOp(models.TextChoices):
    soltero = 'SOLTERO', 'SOLTERO(A)'
    casado = 'CASADO', 'CASADO(A)'
    unionLibre = 'UNION LIBRE', 'UNION LIBRE'
    separado = 'SEPARADO', 'SEPARADO(A)'
    divorciado = 'DIVORCIADO', 'DIVORCIADO(A)'
    viudo = 'VIUDO', 'VIUDO(A)'

class estadoAsociadoOp(models.TextChoices):
    activo = 'ACTIVO', 'ACTIVO'
    inactivo = 'INACTIVO', 'INACTIVO'
    retiro = 'RETIRO', 'RETIRO'

class nivelEducativoOp(models.TextChoices):
    primaria = 'PRIMARIA', 'PRIMARIA'
    secundaria = 'SECUNDARIA', 'SECUNDARIA'
    tecnico = 'TECNICO', 'TECNICO'
    tecnologico = 'TECNOLOGICO', 'TECNOLOGICO'
    pregrado = 'PREGRADO', 'PREGRADO'
    especializacion = 'ESPECIALIZACION', 'ESPECIALIZACION'
    maestria = 'MAESTRIA', 'MAESTRIA'
    doctorado = 'DOCTORADO', 'DOCTORADO'

class tipoViviendaOp(models.TextChoices):
    propia = 'PROPIA', 'PROPIA'
    familiar = 'FAMILIAR', 'FAMILIAR'
    arrendada = 'ARRENDADA', 'ARRENDADA'

class Asociado(models.Model):

    id = models.AutoField(primary_key=True)
    tPersona = models.CharField('Tipo Persona', choices=tipoPersonaOp.choices, default=tipoPersonaOp.pNatural, blank=False, null=False)
    tAsociado = models.ForeignKey(TipoAsociado, on_delete=models.RESTRICT, blank=False, null=False)
    nombre = models.CharField('Nombre', max_length=30, null=False, blank=False)
    apellido = models.CharField('Apellido', max_length=30, null=False, blank=False)
    tipoDocumento = models.CharField('Tipo Documento', choices=tipoDocumentoOp.choices, default=tipoDocumentoOp.cedula, blank=False, null=False)
    numDocumento = models.CharField('Número Documento', max_length=11, blank=False, null=False)
    fechaExpedicion = models.DateField('Fecha Expedicion', blank=False, null=False)
    mpioDoc = models.ForeignKey(Municipio, on_delete=models.RESTRICT, blank=False, null=False)
    nacionalidad = models.CharField('Nacionalidad', max_length=30, null=False, blank=False)
    genero = models.CharField('Genero', choices=generoOp.choices, default=generoOp.masculino, blank=False, null=False)
    estadoCivil = models.CharField('Estado Civil', choices=estadoCivilOp.choices, default=estadoCivilOp.soltero, blank=False, null=False)
    email = models.EmailField('Email', blank=False, null=False)
    fechaNacimiento = models.DateField('Fecha Nacimiento', blank=True, null=True)
    dtoNacimiento = models.ForeignKey(Departamento, on_delete=models.RESTRICT, blank=True, null=True, related_name='dtoNacimiento')
    mpioNacimiento = models.ForeignKey(Municipio, on_delete=models.RESTRICT, blank=True, null=True, related_name='mpioNacimiento')
    tipoVivienda = models.CharField('Tipo Vivienda', choices=tipoViviendaOp.choices, default=tipoViviendaOp.propia, blank=True, null=True)
    estrato = models.IntegerField('Estrato', blank=True, null=True)
    direccion = models.CharField('Dirección', max_length=90, blank=True, null=True)
    barrio = models.CharField('barrio', max_length=90, blank=True, null=True)
    deptoResidencia = models.ForeignKey(Departamento, on_delete=models.RESTRICT, blank=True, null=True, related_name='deptoResidencia')
    mpioResidencia = models.ForeignKey(Municipio, on_delete=models.RESTRICT, blank=True, null=True, related_name='mpioResidencia')
    numResidencia = models.CharField('Numero Residencia', max_length=13, blank=False, null=False)
    indicativoCelular = models.ForeignKey(Pais, on_delete=models.RESTRICT, blank=True, null=True)
    numCelular = models.CharField('Numero Celular', max_length=13, blank=False, null=False)
    envioInfoCorreo = models.BooleanField('Envio Información Email', default=False)
    envioInfoMensaje = models.BooleanField('Envio Información Mensaje Texto', default=False)
    envioInfoWhatsapp = models.BooleanField('Envio Información WhatsApp', default=True)
    nivelEducativo = models.CharField('Nivel Educativo', choices=nivelEducativoOp.choices, default=nivelEducativoOp.secundaria, blank=False, null=False)
    tituloPregrado = models.CharField('Titulo Pregrado', max_length=100, blank=True, null=True)
    tituloPosgrado = models.CharField('Titulo Posgrado', max_length=100, blank=True, null=True)
    estadoAsociado = models.CharField('Estado Asociado', choices=estadoAsociadoOp.choices, default=estadoAsociadoOp.activo, blank=False, null=False)
    nombreRF = models.CharField('Nombre', max_length=50, blank=True, null=True)
    parentesco = models.CharField('Parentesco', max_length=30, blank=True, null=True)
    numContacto = models.CharField('Número', max_length=11, blank=True, null=True)
    estadoRegistro = models.BooleanField('Estado')
    fechaIngreso = models.DateField('Fecha Ingreso', blank=False, null=False)
    fechaRetiro = models.DateField('Fecha Retiro', blank=True, null=True)
    fechaCreacion = models.DateTimeField(auto_now_add=True)
    fechaModificacion = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Asociado'
        ordering = ['pk']
    
    def __str__(self):
        return f"{self.id}"

class Laboral(models.Model):
    
    class Opciones(models.TextChoices):
        si = 'SI', 'SI'
        no = 'NO', 'NO'

    class TipoCuentaOp(models.TextChoices):
        ahorros = 'CUENTA AHORROS', 'CUENTA AHORROS'
        corriente = 'CUENTA CORRIENTE', 'CUENTA CORRIENTE'

    id = models.AutoField(primary_key=True)
    asociado = models.ForeignKey(Asociado, on_delete=models.RESTRICT, blank=False, null=False)
    ocupacion = models.CharField('Ocupacion', max_length=50, blank=True, null=True)
    nombreEmpresa = models.CharField('Nombre Empresa', max_length=50, blank=True, null=True)
    cargo = models.CharField('Dirección', max_length=50, blank=True, null=True)
    nomRepresenLegal = models.CharField('Nombre Representante Legal', max_length=50, blank=True, null=True)
    numDocRL = models.IntegerField('Numero Documento Representante', blank=True, null=True)
    fechaInicio = models.DateField('Fecha Inicio', blank=True, null=True)
    fechaTerminacion = models.DateField('Fecha Terminacion', blank=True, null=True)
    direccion = models.CharField('Direccion', max_length=100, blank=True, null=True)
    mpioTrabajo = models.ForeignKey(Municipio, on_delete=models.RESTRICT, blank=True, null=True)
    dptoTrabajo = models.ForeignKey(Departamento, on_delete=models.RESTRICT, blank=True, null=True)
    telefono = models.CharField('Telefono', blank=True, null=True)
    admRP = models.CharField('Administra RP', choices=Opciones.choices, default=Opciones.no, blank=False, null=False)
    pep = models.CharField('PEP', choices=Opciones.choices, default=Opciones.no, blank=False, null=False)
    activEcono = models.CharField('Actividad Economica', max_length=30, blank=True, null=True)
    ciiu = models.CharField('CIIU', max_length=6, blank=True, null=True)
    banco = models.CharField('Banco', max_length=30, blank=True, null=True)
    numCuenta = models.CharField('Numero Cuenta', max_length=30, blank=True, null=True)
    tipoCuenta = models.CharField('Tipo Cuenta', choices=TipoCuentaOp.choices, default=TipoCuentaOp.ahorros, blank=True, null=True)
    estadoRegistro = models.BooleanField('Estado')
    fechaCreacion = models.DateTimeField(auto_now_add=True)
    fechaModificacion = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Laboral'
        ordering = ['pk']
    
    def __str__(self):
        return  f"{self.asociado}"

class Financiera(models.Model):
    id = models.AutoField(primary_key=True)
    asociado = models.ForeignKey(Asociado, on_delete=models.RESTRICT, blank=False, null=False, related_name="financiera")
    ingresosActPrin = models.IntegerField('Ingresos Actividad Principal', blank=True, null=True)
    otroIngreso1 = models.IntegerField('Otros Ingresos 1', blank=True, null=True)
    otroIngreso2 = models.IntegerField('Otros Ingresos 2', blank=True, null=True)
    egresos = models.IntegerField('Total Egresos', blank=True, null=True)
    activos = models.IntegerField('Total Activos', blank=True, null=True)
    pasivos = models.IntegerField('Total Pasivos', blank=True, null=True)
    patrimonio = models.IntegerField('Total Patrimonio', blank=True, null=True)
    estadoRegistro = models.BooleanField('Estado')
    fechaCreacion = models.DateTimeField(auto_now_add=True)
    fechaModificacion = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Información Financiera'
        ordering = ['pk']
    
    def __str__(self):
        return  f"{self.asociado}"

class TarifaAsociado(models.Model):
    id = models.AutoField(primary_key=True)
    asociado = models.ForeignKey(Asociado, on_delete=models.RESTRICT, blank=False, null=False)
    cuotaAporte = models.IntegerField('Aporte', blank=False, null=False)
    cuotaBSocial = models.IntegerField('Bienestar Social', blank=False, null=False)
    cuotaMascota = models.IntegerField('Mascota', blank=True, null=True)
    cuotaRepatriacion = models.IntegerField('Repatriacion', blank=True, null=True)
    cuotaSeguroVida = models.IntegerField('Seguro Vida', blank=True, null=True)
    fechaInicioAdicional = models.DateField('Fecha Inicio Adicional', blank=True, null=True)
    fechaFinAdicional = models.DateField('Fecha Fin Adicional', blank=True, null=True)
    conceptoAdicional = models.CharField('Concepto Adicional', max_length=100, blank=True, null=True)
    estadoAdicional = models.BooleanField('Estado Adicional')
    cuotaAdicionales = models.IntegerField('Adicionales', blank=True, null=True)
    cuotaCoohopAporte = models.IntegerField('Coohoperativito Aporte', blank=True, null=True)
    cuotaCoohopBsocial = models.IntegerField('Coohoperativito Bienestar Social', blank=True, null=True)
    cuotaConvenio = models.IntegerField('Convenio', blank=True, null=True)
    total = models.IntegerField('Total', blank=False, null=False)
    estadoRegistro = models.BooleanField('Estado')
    fechaCreacion = models.DateTimeField(auto_now_add=True)
    fechaModificacion = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Tarifa Por Asociado'
        verbose_name_plural = 'Tarifa Por Asociado'
        ordering = ['pk']
    
    def __str__(self):
        return f"{self.id}"

class ParametroAsociado(models.Model):
    id = models.AutoField(primary_key=True)
    asociado = models.ForeignKey(Asociado, on_delete=models.RESTRICT, blank=False, null=False)
    autorizaciondcto = models.BooleanField('Estado', blank=True, null=True)
    funeraria = models.ForeignKey(ServicioFuneraria, on_delete=models.RESTRICT, blank=False, null=False)
    primerMes = models.ForeignKey(MesTarifa, on_delete=models.RESTRICT, blank=True, null=True)
    tarifaAsociado = models.ForeignKey(TarifaAsociado, on_delete=models.RESTRICT, blank=True, null=True)
    vinculacionFormaPago = models.ForeignKey(FormaPago, on_delete=models.RESTRICT, blank=True, null=True)
    vinculacionCuotas = models.IntegerField('Vincualacion cuotas', blank=True, null=True)
    vinculacionValor = models.IntegerField('Vinculacion valor', blank=True, null=True)
    vinculacionPendientePago = models.IntegerField('Vinculacion valor', blank=True, null=True)
    estadoRegistro = models.BooleanField('Estado')
    fechaCreacion = models.DateTimeField(auto_now_add=True)
    fechaModificacion = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Parametros Asociado'
        ordering = ['pk']
    
    def __str__(self):
        return  f"{self.asociado}"
    
class RepatriacionTitular(models.Model):
    id = models.AutoField(primary_key=True)
    asociado = models.ForeignKey(Asociado, on_delete=models.RESTRICT, blank=False, null=False)
    paisRepatriacion = models.ForeignKey(PaisRepatriacion, on_delete=models.RESTRICT, blank=True, null=True)
    fechaRepatriacion = models.DateField(blank=False, null=False)
    ciudadRepatriacion = models.CharField(max_length=50, blank=True, null=True)
    fechaRetiro = models.DateField(blank=True, null=True)
    estadoRegistro = models.BooleanField('Estado')
    fechaCreacion = models.DateTimeField(auto_now_add=True)
    fechaModificacion = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Repatriacion Titular'
        ordering = ['pk']

class ConveniosAsociado(models.Model):
    id = models.AutoField(primary_key=True)
    convenio = models.ForeignKey(Convenio, on_delete=models.RESTRICT, blank=False, null=False)
    asociado = models.ForeignKey(Asociado, on_delete=models.RESTRICT, blank=False, null=False)
    primerMes = models.ForeignKey(MesTarifa, on_delete=models.RESTRICT, blank=False, null=False)
    fechaIngreso = models.DateField('Fecha Ingreso', blank=False, null=False)
    fechaRetiro = models.DateField('Fecha Retiro', blank=True, null=True)
    estadoRegistro = models.BooleanField('Estado')
    fechaCreacion = models.DateTimeField(auto_now_add=True)
    fechaModificacion = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Convenios Asociado'
        ordering = ['pk']

class ConvenioHistoricoGasolina(models.Model):
    id = models.AutoField(primary_key=True)
    asociado = models.ForeignKey(Asociado, on_delete=models.RESTRICT, blank=False, null=False)
    convenio = models.ForeignKey(ConveniosAsociado, on_delete=models.RESTRICT, blank=False, null=False)
    mes_tarifa = models.ForeignKey(MesTarifa, on_delete=models.RESTRICT, blank=False, null=False)
    valor_pagar = models.IntegerField('Valor', blank=True, null=True)
    pendiente_pago = models.IntegerField('Valor', blank=True, null=True)
    estado_registro = models.BooleanField('Estado')
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Convenio Chip Gasolina'
        ordering = ['pk']