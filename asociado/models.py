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

class zonaUbicacionOp(models.TextChoices):
    RURAL = 'RURAL', 'RURAL'
    URBANA = 'URBANA', 'URBANA'

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
    zonaUbicacion = models.CharField(choices=zonaUbicacionOp.choices, blank=True, null=True, default=zonaUbicacionOp.URBANA, max_length=6)
    empleadoCooho = models.CharField(max_length=2, default='NO', blank=True, null=True)
    nPersonasCargo = models.IntegerField('Número Personas a Cargo', blank=True, null=True)
    nHijos = models.IntegerField('Número Hijos', blank=True, null=True)
    cabezaFamilia = models.CharField(max_length=2, default='NO', blank=True, null=True)
    fechaIngreso = models.DateField('Fecha Ingreso', blank=False, null=False)
    fechaActualizacionDatos = models.DateField('Fecha Actualizacion Datos', blank=True, null=True)
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

    class OcupacionOp(models.TextChoices):
        estudiante = 'ESTUDIANTE', 'ESTUDIANTE'
        empleado = 'EMPLEADO', 'EMPLEADO'
        pensionado = 'PENSIONADO', 'PENSIONADO'
        independiente = 'INDEPENDIENTE', 'INDEPENDIENTE'
        comerciante = 'COMERCIANTE', 'COMERCIANTE'
        hogar = 'HOGAR', 'HOGAR'
        cesante = 'CESANTE', 'CESANTE'
        otro = 'OTRO', 'OTRO'
    
    class TipoEmpresaOp(models.TextChoices):
        publica = 'PUBLICA', 'PUBLICA'
        privada = 'PRIVADA', 'PRIVADA'
        mixta = 'MIXTA', 'MIXTA'
        otro = 'OTRO', 'OTRO'
    
    class TipoContratoOp(models.TextChoices):
        indefinido = 'INDEFINIDO', 'INDEFINIDO'
        terminoFijo = 'TERMINO FIJO', 'TERMINO FIJO'
        obraLabor = 'OBRA O LABOR', 'OBRA O LABOR'
        prestacionServicios = 'PRESTACION DE SERVICIOS', 'PRESTACION DE SERVICIOS'
        honorarios = 'HONORARIOS', 'HONORARIOS'

    id = models.AutoField(primary_key=True)
    asociado = models.ForeignKey(Asociado, on_delete=models.RESTRICT, blank=False, null=False)
    ocupacion = models.CharField(choices=OcupacionOp.choices, default=OcupacionOp.empleado, max_length=50, blank=True, null=True)
    ocupacionOtro = models.CharField('Otra Ocupacion', max_length=50, blank=True, null=True)
    tipoEmpresa = models.CharField(choices=TipoEmpresaOp.choices, default=TipoEmpresaOp.publica, max_length=50, blank=True, null=True)
    tipoEmpresaOtro = models.CharField('Otro Tipo Empresa', max_length=50, blank=True, null=True)
    nombreEmpresa = models.CharField('Nombre Empresa', max_length=50, blank=True, null=True)
    cargo = models.CharField('Dirección', max_length=50, blank=True, null=True)
    tipoContrato = models.CharField(choices=TipoContratoOp.choices, default=TipoContratoOp.indefinido, max_length=30, blank=True, null=True)
    fechaInicio = models.DateField('Fecha Inicio', blank=True, null=True)
    fechaTerminacion = models.DateField('Fecha Terminacion', blank=True, null=True)
    nomRepresenLegal = models.CharField('Nombre Representante Legal', max_length=50, blank=True, null=True)
    numDocRL = models.IntegerField('Numero Documento Representante', blank=True, null=True)
    nomJefeInmediato = models.CharField('Nombre Jefe Inmediato', max_length=50, blank=True, null=True)
    telefonoJefeInmediato = models.CharField('Telefono Jefe Inmediato', blank=True, null=True)
    direccion = models.CharField('Direccion', max_length=100, blank=True, null=True)
    dptoTrabajo = models.ForeignKey(Departamento, on_delete=models.RESTRICT, blank=True, null=True)
    mpioTrabajo = models.ForeignKey(Municipio, on_delete=models.RESTRICT, blank=True, null=True)
    telefonoLaboral = models.CharField('Telefono', blank=True, null=True)
    correoLaboral = models.EmailField('Correo', blank=True, null=True)
    admRP = models.CharField('Administra RP', choices=Opciones.choices, default=Opciones.no, blank=False, null=False)
    pep = models.CharField('PEP', choices=Opciones.choices, default=Opciones.no, blank=False, null=False)
    activEcono = models.CharField('Actividad Economica', max_length=30, blank=True, null=True)
    ciiu = models.CharField('CIIU', max_length=6, blank=True, null=True)
    declaraRenta = models.CharField('Declara Renta', choices=Opciones.choices, default=Opciones.no, blank=False, null=False)
    responsableIva = models.CharField('Responsable IVA', choices=Opciones.choices, default=Opciones.no, blank=False, null=False)
    regimenTributario = models.CharField('Regimen Tributario', max_length=30, blank=True, null=True)
    banco = models.CharField('Banco', max_length=30, blank=True, null=True)
    tipoCuenta = models.CharField('Tipo Cuenta', choices=TipoCuentaOp.choices, blank=True, null=True)
    numCuenta = models.CharField('Numero Cuenta', max_length=30, blank=True, null=True)
    estadoRegistro = models.BooleanField('Estado')
    fechaCreacion = models.DateTimeField(auto_now_add=True)
    fechaModificacion = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Laboral'
        ordering = ['pk']
    
    def __str__(self):
        return  f"{self.asociado}"

class Financiera(models.Model):

    class Opciones(models.TextChoices):
        si = 'SI', 'SI'
        no = 'NO', 'NO'

    id = models.AutoField(primary_key=True)
    asociado = models.ForeignKey(Asociado, on_delete=models.RESTRICT, blank=False, null=False, related_name="financiera")
    ingrSalario = models.IntegerField('Ingreso Salario', blank=True, null=True)
    ingrHorasExtras = models.IntegerField('Ingreso Horas Extras', blank=True, null=True)
    ingrPension = models.IntegerField('Ingreso Pension', blank=True, null=True)
    ingrCompensacion = models.IntegerField('Ingreso Compensacion', blank=True, null=True)
    ingrHonorarios = models.IntegerField('Ingreso Honorarios', blank=True, null=True)
    ingrVentas = models.IntegerField('Ingreso Ventas', blank=True, null=True)
    ingrIntereses = models.IntegerField('Ingreso Intereses', blank=True, null=True)
    ingrGiros = models.IntegerField('Ingreso Giros', blank=True, null=True)
    ingrArrendamientos = models.IntegerField('Ingreso Arrendamientos', blank=True, null=True)
    ingrOtros = models.IntegerField('Ingreso Otros', blank=True, null=True)
    ingrDescripcionOtros = models.CharField('Descripcion Otros Ingresos', max_length=40, blank=True, null=True)
    egrArrendamiento = models.IntegerField('Egreso Arrendamientos', blank=True, null=True)
    egrServiciosPublicos = models.IntegerField('Egreso Arrendamientos', blank=True, null=True)
    egrAportesSalud = models.IntegerField('Egreso Aportes Salud', blank=True, null=True)
    egrTransporte = models.IntegerField('Egreso Transporte', blank=True, null=True)
    egrAlimentacion = models.IntegerField('Egreso Alimentacion', blank=True, null=True)
    egrObligaciones = models.IntegerField('Egreso Obligaciones', blank=True, null=True)
    egrTarjetas = models.IntegerField('Egreso Tarjeta Credito', blank=True, null=True)
    egrCostos = models.IntegerField('Egreso Costos y gastos ventas', blank=True, null=True)
    egrEmbargos = models.IntegerField('Egreso Embargo', blank=True, null=True)
    egrOtros = models.IntegerField('Egreso Otros', blank=True, null=True)
    egrDescripcionOtros = models.CharField('Descripcion Otros Egresos', max_length=40, blank=True, null=True)
    operacionesMonedaExtranjera = models.CharField('Operaciones Moneda Extranjera', choices=Opciones.choices, default=Opciones.no, blank=True, null=True)
    operacionesMonedaCuales = models.CharField('Operaciones Moneda Cuales', max_length=50, blank=True, null=True)
    operacionesMonedaTipo = models.CharField('Tipo producto u operacion', max_length=50, blank=True, null=True)
    operacionesMonedaMonto = models.IntegerField('Monto', blank=True, null=True)
    operacionesMoneda = models.CharField('Tipo Moneda Extranjera', max_length=50, blank=True, null=True)
    poseeCuentasMonedaExtranjera = models.CharField('Posee Cuentas Moneda Extranjera', choices=Opciones.choices, default=Opciones.no, blank=True, null=True)
    poseeCuentasBanco = models.CharField('Posee Cuentas en Otros Bancos', max_length=50, blank=True, null=True)
    poseeCuentasCuenta = models.IntegerField('Cuenta', blank=True, null=True)
    poseeCuentasMoneda = models.CharField('Moneda', max_length=50, blank=True, null=True)
    poseeCuentasCiudad = models.CharField('Ciudad', max_length=50, blank=True, null=True)
    poseeCuentasPais = models.CharField('Pais', max_length=50, blank=True, null=True)
    estadoRegistro = models.BooleanField('Estado')
    fechaCreacion = models.DateTimeField(auto_now_add=True)
    fechaModificacion = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Información Financiera'
        ordering = ['pk']
    
    def __str__(self):
        return  f"{self.asociado}"
    
    @property
    def total_ingresos(self):
        campos = [
            self.ingrSalario, self.ingrHorasExtras, self.ingrPension, self.ingrCompensacion, self.ingrHonorarios, self.ingrVentas, self.ingrIntereses, self.ingrGiros, self.ingrArrendamientos, self.ingrOtros
        ]
        return sum(filter(None, campos))
    
    @property
    def total_egresos(self):
        campos = [
            self.egrArrendamiento, self.egrServiciosPublicos, self.egrAportesSalud,
            self.egrTransporte, self.egrAlimentacion, self.egrObligaciones,
            self.egrTarjetas, self.egrCostos, self.egrEmbargos, self.egrOtros
        ]
        return sum(filter(None, campos))
    
    @property
    def total_patrimonio(self):
        return (self.total_ingresos or 0) - (self.total_egresos or 0)


class TarifaAsociado(models.Model):
    id = models.AutoField(primary_key=True)
    asociado = models.ForeignKey(Asociado, on_delete=models.RESTRICT, blank=False, null=False)
    cuotaAporte = models.IntegerField('Aporte', blank=False, null=False)
    cuotaBSocial = models.IntegerField('Bienestar Social', blank=False, null=False)
    cuotaMascota = models.IntegerField('Mascota', blank=True, null=True)
    cuotaRepatriacionBeneficiarios = models.IntegerField('Repatriacion Beneficiarios', blank=True, null=True)
    cuotaRepatriacionTitular = models.IntegerField('Repatriacion Titular', blank=True, null=True,default=0)
    cuotaSeguroVida = models.IntegerField('Seguro Vida', blank=True, null=True)
    fechaInicioAdicional = models.DateField('Fecha Inicio Adicional', blank=True, null=True)
    fechaFinAdicional = models.DateField('Fecha Fin Adicional', blank=True, null=True)
    primerMesCuotaAdicional = models.ForeignKey(
        MesTarifa,
        on_delete=models.RESTRICT,
        blank=True,
        null=True,
        related_name='tarifa_asociado'
    )
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
    primerMes = models.ForeignKey(
        MesTarifa,
        on_delete=models.RESTRICT,
        blank=True,
        null=True,
        related_name='repatriaciones_titular'
    )
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


class RadicadoAsociado(models.Model):
    TIPO_CHOICES = [
        ('RA', 'Registro Asociado'),
        ('RSE', 'Registro Servicios Exequiales'),
        ('SAE', 'Solicitud Auxilio Económico'),
        ('FEP', 'Formato Extracto Pago'),
        ('FSC', 'Formato Solicitud Crédito'),
    ]

    PROCESO_CHOICES = [
        ('VINCULACION', 'Vinculación'),
        ('ACTUALIZACION', 'Actualización de datos'),
        ('SOLICITUD', 'Solicitud general'),
    ]

    asociado = models.ForeignKey('Asociado', on_delete=models.CASCADE, related_name='radicados')
    tipo = models.CharField(max_length=10, choices=TIPO_CHOICES, blank=True, null=True)
    radicado = models.CharField(max_length=20, unique=True)
    proceso = models.CharField(max_length=20, choices=PROCESO_CHOICES, blank=True, null=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.radicado} - {self.asociado}"