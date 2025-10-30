from django.db import models

# Create your models here.


class TipoAuxilio(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField("Nombre", max_length=50, null=False, blank=False)
    valor = models.IntegerField("Valor", blank=False, null=False)
    estadoRegistro = models.BooleanField("Estado")

    class Meta:
        verbose_name = "Tipo Auxilio"
        verbose_name_plural = "Tipo Auxilio"
        ordering = ["pk"]

    def __str__(self):
        return self.nombre


class Tarifas(models.Model):
    id = models.AutoField(primary_key=True)
    concepto = models.CharField("Concepto", max_length=30, null=False, blank=False)
    cuenta = models.IntegerField("Cuenta", null=False, blank=False)
    valor = models.IntegerField("Valor", null=False, blank=False)
    estadoRegistro = models.BooleanField("Estado")

    class Meta:
        verbose_name = "Tarifa"
        verbose_name_plural = "Tarifas"
        ordering = ["pk"]

    def __str__(self):
        return self.concepto


class MesTarifa(models.Model):
    id = models.AutoField(primary_key=True)
    concepto = models.CharField("Concepto", max_length=30, null=False, blank=False)
    aporte = models.IntegerField("Aporte", blank=False, null=False)
    bSocial = models.IntegerField("Bienestar Social", blank=False, null=False)
    fechaInicio = models.DateField("Fecha Inicio", blank=True, null=True)
    fechaFinal = models.DateField("Fecha Final", blank=True, null=True)

    class Meta:
        verbose_name = "Tarifa Por Mes"
        verbose_name_plural = "Tarifa Por Mes"
        ordering = ["pk"]

    def __str__(self):
        return self.concepto


class FormaPago(models.Model):
    id = models.AutoField(primary_key=True)
    formaPago = models.CharField("Forma Pago", max_length=30, null=False, blank=False)
    estadoRegistro = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Forma de Pago"
        verbose_name_plural = "Forma de Pago"
        ordering = ["pk"]

    def __str__(self):
        return self.formaPago


class TipoAsociado(models.Model):
    id = models.AutoField(primary_key=True)
    concepto = models.CharField("Tipo Asociado", max_length=30, null=False, blank=False)

    class Meta:
        verbose_name = "Tipo Asociado"
        verbose_name_plural = "Tipo Asociado"
        ordering = ["pk"]

    def __str__(self):
        return self.concepto


class ServicioFuneraria(models.Model):
    id = models.AutoField(primary_key=True)
    concepto = models.CharField(
        "Servicio Funerario", max_length=30, null=False, blank=False
    )

    class Meta:
        verbose_name = "Servicio Funeraria"
        verbose_name_plural = "Servicio Funeraria"
        ordering = ["pk"]

    def __str__(self):
        return self.concepto


class Convenio(models.Model):
    id = models.AutoField(primary_key=True)
    fechaInicio = models.DateField("Fecha Inicio", null=False, blank=False)
    concepto = models.CharField(
        "Convenio Asociado", max_length=30, null=False, blank=False
    )
    valor = models.IntegerField("Valor", null=False, blank=False)
    fechaTerminacion = models.DateField("Fecha Terminacion", null=True, blank=True)
    estado = models.BooleanField("Estado", default=True)

    class Meta:
        verbose_name = "Convenio Asociado"
        verbose_name_plural = "Convenio Asociado"
        ordering = ["pk"]

    def __str__(self):
        return self.concepto


class TasasInteresCredito(models.Model):
    id = models.AutoField(primary_key=True)
    concepto = models.CharField("Concepto", max_length=30, null=False, blank=False)
    porcentaje = models.DecimalField(
        max_digits=6, decimal_places=5, blank=False, null=False
    )

    class Meta:
        verbose_name = "Tasas Interes Credito"
        verbose_name_plural = "Tasas Interes Credito"
        ordering = ["pk"]

    def __str__(self):
        return self.concepto


class ConsecutivoRadicado(models.Model):
    tipo = models.CharField(max_length=10)
    anio = models.IntegerField()
    ultimo_numero = models.IntegerField(default=0)

    class Meta:
        unique_together = ("tipo", "anio")
        verbose_name = "Consecutivo de Radicado"
        verbose_name_plural = "Consecutivos de Radicados"

    def __str__(self):
        return f"{self.tipo}-{self.anio}-{self.ultimo_numero:05d}"
