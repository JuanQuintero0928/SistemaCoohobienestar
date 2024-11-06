from django.db import models

# Create your models here.

class Departamento(models.Model):
    id = models.AutoField(primary_key=True)
    codigo = models.CharField('Codigo Depto', blank=False, null=False, default=0)
    nombre = models.CharField('Departamento', max_length=30, null=False, blank=False)

    class Meta:
        ordering = ['pk']

    def __str__(self):
        return self.nombre

class Municipio(models.Model):
    id = models.AutoField(primary_key=True)
    codigo = models.CharField('Codigo Mpio', blank=False, null=False, default=0)
    nombre = models.CharField('Municipio', max_length=30, null=False, blank=False)
    departamento = models.ForeignKey(Departamento, on_delete=models.RESTRICT, blank=False, null=False)

    class Meta:
        ordering = ['pk']

    def __str__(self):
        return self.nombre
    
class PaisRepatriacion(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField('Pais', max_length=30, null=False, blank=False)
    
    class Meta:
        ordering = ['pk']
        verbose_name = 'Pais Repatriación'
        verbose_name_plural = 'Pais Repatriación'

    def __str__(self):
        return self.nombre