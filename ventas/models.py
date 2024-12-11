from django.db import models
from django.contrib.auth.models import User

from asociado.models import Asociado
import historico

# Create your models here.

class Categoria(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre

class Proveedor(models.Model):
    id = models.AutoField(primary_key=True)
    nit = models.CharField(max_length=18)
    razonSocial = models.CharField(max_length=100)

    def __str__(self):
        return self.razonSocial

class Producto(models.Model):
    id = models.AutoField(primary_key=True)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, blank=False, null=False)
    nombre = models.CharField(max_length=100, blank=False, null=False)
    referencia = models.CharField(max_length=20, blank=False, null=False)
    ean = models.CharField(max_length=13, blank=False, null=False)
    descripcion = models.CharField(max_length=200, blank=False, null=False)
    precio = models.IntegerField(blank=False, null=False)
    descuento = models.DecimalField(max_digits=3, decimal_places=2, blank=True, null=True)
    proveedor = models.ForeignKey(Proveedor, on_delete=models.CASCADE, blank=False, null=False)
    inventario = models.BooleanField(default=False)
    stock = models.IntegerField(blank=False, null=False)
    estadoRegistro = models.BooleanField(default=True)
    
    def __str__(self):
        return self.nombre
    
class HistoricoVenta(models.Model):

    class FormaPago(models.TextChoices):
        contado = 'CONTADO', 'CONTADO'
        credito = 'CREDITO', 'CREDITO'

    id = models.AutoField(primary_key=True)
    asociado = models.ForeignKey(Asociado, on_delete=models.CASCADE, blank=False, null=False)
    fechaVenta = models.DateField(blank=False, null=False)
    valorBruto = models.IntegerField(blank=False, null=False)
    formaPago = models.CharField(choices=FormaPago.choices, default=FormaPago.contado, blank=False, null=False)
    valorNeto = models.IntegerField(blank=False, null=False)
    userCreacion = models.ForeignKey(User, on_delete=models.CASCADE, blank=False, null=False)
    estadoRegistro = models.BooleanField(default=True)
    fechaCreacion = models.DateTimeField(auto_now_add=True)
    fechaModificacion = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.fechaVenta} {self.asociado.numDocumento}"
    
class DetalleVenta(models.Model):
    id = models.AutoField(primary_key=True)
    historicoVenta = models.ForeignKey(HistoricoVenta, on_delete=models.CASCADE, blank=False, null=False)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, blank=False, null=False)
    cantidad = models.IntegerField(blank=False, null=False)
    precio = models.IntegerField(blank=False, null=False)
    totalBruto = models.IntegerField(blank=False, null=False)
    descuento = models.DecimalField(max_digits=3, decimal_places=2, blank=True, null=True)
    totalNeto = models.IntegerField(blank=False, null=False)
    
    def __str__(self):
        return f"{self.historicoVenta.id} {self.producto.nombre}"