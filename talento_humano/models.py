from django.db import models


class tipo_documento_op(models.TextChoices):
    cedula = "CEDULA", "CEDULA"
    cedulaExtranjera = "CEDULA EXTRANJERA", "CEDULA EXTRANJERA"
    pasaporte = "PASAPORTE", "PASAPORTE"
    ppt = "PPT", "PPT"


class Empleados(models.Model):
    nombre = models.CharField(max_length=30, blank=False, null=False)
    apellido = models.CharField(max_length=30, blank=False, null=False)
    tipo_documento = models.CharField(
        max_length=20,
        choices=tipo_documento_op.choices,
        default=tipo_documento_op.cedula,
        blank=False,
        null=False,
    )
    numero_documento = models.CharField(max_length=20, blank=False, null=False)
    fecha_nacimiento = models.DateField(blank=False, null=False)
    celular = models.CharField(max_length=20, blank=False, null=False)
    correo = models.EmailField(max_length=254, blank=False, null=False)
    direccion = models.CharField(max_length=100, blank=False, null=False)
    departamento = models.CharField(max_length=50, blank=False, null=False)
    municipio = models.CharField(max_length=50, blank=False, null=False)
    estado_registro = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.nombre} {self.apellido}"

    def save(self, *args, **kwargs):
        # Convertir campos a mayúsculas antes de guardar
        self.nombre = self.nombre.upper()
        self.apellido = self.apellido.upper()
        self.direccion = self.direccion.upper()
        self.departamento = self.departamento.upper()
        self.municipio = self.municipio.upper()
        super().save(*args, **kwargs)


class Area(models.Model):
    nombre = models.CharField(max_length=50, blank=False, null=False)

    def __str__(self):
        return self.nombre

    def save(self, *args, **kwargs):
        # Convertir el nombre a mayúsculas antes de guardar
        self.nombre = self.nombre.upper()
        super().save(*args, **kwargs)


class Cargo(models.Model):
    nombre = models.CharField(max_length=50, blank=False, null=False)

    def __str__(self):
        return self.nombre

    def save(self, *args, **kwargs):
        # Convertir el nombre a mayúsculas antes de guardar
        self.nombre = self.nombre.upper()
        super().save(*args, **kwargs)


class TipoContrato(models.Model):
    nombre = models.CharField(max_length=50, blank=False, null=False)

    def __str__(self):
        return self.nombre

    def save(self, *args, **kwargs):
        # Convertir el nombre a mayúsculas antes de guardar
        self.nombre = self.nombre.upper()
        super().save(*args, **kwargs)


class NombreUnidad(models.Model):
    nombre = models.CharField(max_length=50, blank=False, null=False)

    def __str__(self):
        return self.nombre

    def save(self, *args, **kwargs):
        # Convertir el nombre a mayúsculas antes de guardar
        self.nombre = self.nombre.upper()
        super().save(*args, **kwargs)


class HistorialLaboral(models.Model):
    empleado = models.ForeignKey(Empleados, on_delete=models.RESTRICT)
    area = models.ForeignKey(Area, on_delete=models.RESTRICT)
    cargo = models.ForeignKey(Cargo, on_delete=models.RESTRICT)
    tipo_contrato = models.ForeignKey(TipoContrato, on_delete=models.RESTRICT)
    nombre_unidad = models.ForeignKey(NombreUnidad, on_delete=models.RESTRICT)
    fecha_inicio = models.DateField(blank=False, null=False)
    fecha_fin = models.DateField(blank=True, null=True)
    salario = models.IntegerField(blank=False, null=False)
    estado_registro = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Histórico Laboral de {self.empleado}"
