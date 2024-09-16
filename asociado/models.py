from django.db import models
from departamento.models import Departamento, Municipio
from parametro.models import TipoAsociado, ServicioFuneraria, MesTarifa
# from historico.models import TarifaAsociado

# Create your models here.

class Asociado(models.Model):

    class tipoPersonaOp(models.TextChoices):
        pNatural = 'PERSONA NATURAL', 'PERSONA NATURAL'
        pjuridica = 'PERSONA JURIDICA', 'PERSONA JURIDICA'

    class tipoDocumentoOp(models.TextChoices):
        cedula = 'CEDULA', 'CEDULA' 
        registroCivil = 'REGISTRO CIVIL', 'REGISTRO CIVIL'
        tarjetaIdentidad = 'TARJETA IDENTIDAD', 'TARJETA IDENTIDAD'
        cedulaExtranjera = 'CEDULA EXTRANJERA', 'CEDULA EXTRANJERA'
        pasaporte = 'PASAPORTE', 'PASAPORTE'
    
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
        retirado = 'RETIRADO', 'RETIRADO'

    class nivelEducativoOp(models.TextChoices):
        primaria = 'PRIMARIA', 'PRIMARIA'
        secundaria = 'SECUNDARIA', 'SECUNDARIA'
        tecnico = 'TECNICO', 'TECNICO'
        tecnologico = 'TECNOLOGICO', 'TECNOLOGICO'
        pregrado = 'PREGRADO', 'PREGRADO'
        especializacion = 'ESPECIALIZACION', 'ESPECIALIZACION'
        maestria = 'MAESTRIA', 'MAESTRIA'
        doctorado = 'DOCTORADO', 'DOCTORADO'

    id = models.AutoField(primary_key=True)
    tPersona = models.CharField('Tipo Persona', choices=tipoPersonaOp.choices, default=tipoPersonaOp.pNatural, blank=False, null=False)
    tAsociado = models.ForeignKey(TipoAsociado, on_delete=models.RESTRICT, blank=False, null=False)
    nombre = models.CharField('Nombre', max_length=30, null=False, blank=False)
    apellido = models.CharField('Apellido', max_length=30, null=False, blank=False)
    tipoDocumento = models.CharField('Tipo Documento', choices=tipoDocumentoOp.choices, default=tipoDocumentoOp.cedula, blank=False, null=False)
    numDocumento = models.CharField('Número Documento', max_length=10, blank=False, null=False)
    fechaExpedicion = models.DateField('Fecha Expedicion', blank=False, null=False)
    mpioDoc = models.ForeignKey(Municipio, on_delete=models.RESTRICT, blank=False, null=False)
    nacionalidad = models.CharField('Nacionalidad', max_length=30, null=False, blank=False)
    genero = models.CharField('Genero', choices=generoOp.choices, default=generoOp.masculino, blank=False, null=False)
    estadoCivil = models.CharField('Estado Civil', choices=estadoCivilOp.choices, default=estadoCivilOp.soltero, blank=False, null=False)
    email = models.EmailField('Email', blank=False, null=False)
    numResidencia = models.CharField('Numero Residencia', max_length=11, blank=False, null=False)
    numCelular = models.CharField('Numero Celular', max_length=11, blank=False, null=False)
    envioInfoCorreo = models.BooleanField('Envio Información Email', default=False)
    envioInfoMensaje = models.BooleanField('Envio Información Mensaje Texto', default=False)
    envioInfoWhatsapp = models.BooleanField('Envio Información WhatsApp', default=True)
    nivelEducativo = models.CharField('Nivel Educativo', choices=nivelEducativoOp.choices, default=nivelEducativoOp.secundaria, blank=False, null=False)
    tituloPregrado = models.CharField('Titulo Pregrado', max_length=100, blank=True, null=True)
    tituloPosgrado = models.CharField('Titulo Posgrado', max_length=100, blank=True, null=True)
    estadoAsociado = models.CharField('Estado Asociado', choices=estadoAsociadoOp.choices, default=estadoAsociadoOp.activo, blank=False, null=False)
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
    
class Nacimiento(models.Model):
    id = models.AutoField(primary_key=True)
    asociado = models.ForeignKey(Asociado, on_delete=models.RESTRICT, blank=False, null=False)
    fechaNacimiento = models.DateField('Fecha Nacimiento', blank=False, null=False)
    dtoNacimiento = models.ForeignKey(Departamento, on_delete=models.RESTRICT, blank=False, null=False)
    mpioNacimiento = models.ForeignKey(Municipio, on_delete=models.RESTRICT, blank=False, null=False)
    
    class Meta:
        verbose_name = 'Fecha Nacimiento'
        ordering = ['pk']
    
    def __str__(self):
        return  f"{self.fechaNacimiento}"


class Residencia(models.Model):

    class tipoViviendaOp(models.TextChoices):
        propia = 'PROPIA', 'PROPIA'
        familiar = 'FAMILIAR', 'FAMILIAR'
        arrendada = 'ARRENDADA', 'ARRENDADA'

    id = models.AutoField(primary_key=True)
    asociado = models.ForeignKey(Asociado, on_delete=models.RESTRICT, blank=False, null=False)
    tipoVivienda = models.CharField('Tipo Vivienda', choices=tipoViviendaOp.choices, default=tipoViviendaOp.propia, blank=False, null=False)
    estrato = models.IntegerField('Estrato', blank=False, null=False)
    direccion = models.CharField('Dirección', max_length=50, blank=False, null=False)
    barrio = models.CharField('barrio', max_length=50, blank=False, null=False)
    deptoResidencia = models.ForeignKey(Departamento, on_delete=models.RESTRICT, blank=False, null=False)
    mpioResidencia = models.ForeignKey(Municipio, on_delete=models.RESTRICT, blank=False, null=False)
    estadoRegistro = models.BooleanField('Estado')
    fechaCreacion = models.DateTimeField(auto_now_add=True)
    fechaModificacion = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Residencia'
        ordering = ['pk']
    
    def __str__(self):
        return  f"{self.asociado}"

class Laboral(models.Model):
    
    class Opciones(models.TextChoices):
        si = 'SI', 'SI'
        no = 'NO', 'NO'

    class TipoCuentaOp(models.TextChoices):
        ahorros = 'CUENTA AHORROS', 'CUENTA AHORROS'
        corriente = 'CUENTA CORRIENTE', 'CUENTA CORRIENTE'

    id = models.AutoField(primary_key=True)
    asociado = models.ForeignKey(Asociado, on_delete=models.RESTRICT, blank=False, null=False)
    ocupacion = models.CharField('Ocupacion', max_length=50, blank=False, null=False)
    nombreEmpresa = models.CharField('Nombre Empresa', max_length=50, blank=True, null=True)
    cargo = models.CharField('Dirección', max_length=50, blank=True, null=True)
    nomRepresenLegal = models.CharField('Nombre Representante Legal', max_length=50, blank=True, null=True)
    numDocRL = models.IntegerField('Numero Documento Representante', blank=True, null=True)
    fechaInicio = models.DateField('Fecha Inicio', blank=True, null=True)
    fechaTerminacion = models.DateField('Fecha Terminacion', blank=True, null=True)
    direccion = models.CharField('Direccion', max_length=100, blank=True, null=True)
    mpioTrabajo = models.ForeignKey(Municipio, on_delete=models.RESTRICT, blank=True, null=True)
    dptoTrabajo = models.ForeignKey(Departamento, on_delete=models.RESTRICT, blank=True, null=True)
    telefono = models.IntegerField('Telefono', blank=True, null=True)
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
    asociado = models.ForeignKey(Asociado, on_delete=models.RESTRICT, blank=False, null=False)
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

class ReferenciaFamiliar(models.Model):
    id = models.AutoField(primary_key=True)
    asociado = models.ForeignKey(Asociado, on_delete=models.RESTRICT, blank=False, null=False)
    nombre = models.CharField('Nombre', max_length=50, blank=True, null=True)
    parentesco = models.CharField('Parentesco', max_length=30, blank=True, null=True)
    numContacto = models.CharField('Número', max_length=11, blank=True, null=True)
    estadoRegistro = models.BooleanField('Estado')
    fechaCreacion = models.DateTimeField(auto_now_add=True)
    fechaModificacion = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Referencia Familiar'
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
    cuotaAdicionales = models.IntegerField('Adicionales', blank=True, null=True)
    cuotaCoohopAporte = models.IntegerField('Coohoperativito Aporte', blank=True, null=True)
    cuotaCoohopBsocial = models.IntegerField('Coohoperativito Bienestar Social', blank=True, null=True)
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
    empresa = models.ForeignKey(TipoAsociado, on_delete=models.RESTRICT, blank=True, null=True)
    autorizaciondcto = models.BooleanField('Estado', blank=True, null=True)
    funeraria = models.ForeignKey(ServicioFuneraria, on_delete=models.RESTRICT, blank=False, null=False)
    primerMes = models.ForeignKey(MesTarifa, on_delete=models.RESTRICT, blank=True, null=True)
    tarifaAsociado = models.ForeignKey(TarifaAsociado, on_delete=models.RESTRICT, blank=True, null=True)
    estadoRegistro = models.BooleanField('Estado')
    fechaCreacion = models.DateTimeField(auto_now_add=True)
    fechaModificacion = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Parametros Asociado'
        ordering = ['pk']
    
    def __str__(self):
        return  f"{self.asociado}"
    
