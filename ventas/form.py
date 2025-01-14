from tkinter import Widget
from django import forms
from .models import Producto, HistoricoVenta, DetalleVenta

class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['categoria',
                  'nombre',
                  'referencia',
                  'ean',
                  'descripcion',
                  'precio',
                  'proveedor',
                  'stock',
        ]
        widgets = {
            'categoria': forms.Select(attrs={'class': 'form-control'}),
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre del producto', 'style': 'text-transform: uppercase;'}),
            'referencia': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Referencia'}),
            'ean': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Código EAN'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Descripción del producto'}),
            'precio': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Precio en pesos', 'min': 0}),
            'proveedor': forms.Select(attrs={'class': 'form-control'}),
            'stock': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Cantidad en stock', 'min': 0}),
        }
        labels = {
            'categoria': 'Categoría',
            'nombre': 'Nombre del producto',
            'referencia': 'Referencia',
            'ean': 'Código EAN',
            'descripcion': 'Descripción',
            'precio': 'Precio',
            'proveedor': 'Proveedor',
            'stock': 'Stock disponible'
        }

class HistoricoVentaForm(forms.ModelForm):
    class Meta:
        model = HistoricoVenta
        fields = ['fechaVenta',
                  'formaPago',
                  'cuotas',
                  'descuento',
                  'valorBruto',
                  'valorNeto',
        ]
        widgets = {
            'fechaVenta': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'},format='%Y-%m-%d',),
            'formaPago': forms.Select(attrs={'class': 'form-control'}),
            'cuotas': forms.NumberInput(attrs={'class': 'form-control', 'min':2, 'max':3}),
            'descuento': forms.Select(attrs={'class': 'form-control','disabled':'disabled'}),
            'valorBruto': forms.NumberInput(attrs={'class': 'form-control', 'readonly':'readonly'}),
            'valorNeto': forms.TextInput(attrs={'class': 'form-control', 'readonly':'readonly'}),
        }
        labels = {
            'fechaVenta': 'Fecha Venta',
            'formaPago': 'Forma Pago',
            'cuotas': 'Número Cuotas',
            'descuento': 'Descuento (%)',
            'valorBruto': 'Valor Bruto',
            'valorNeto': 'Valor Neto',
        }

class DetalleVentaForm(forms.ModelForm):
    
    class Meta:
        model = DetalleVenta
        fields = ['producto',
                  'cantidad',
        ]
        widgets = {
            'producto': forms.Select(attrs={'class': 'form-control'}),
            'cantidad': forms.NumberInput(attrs={'class':'form-control', 'min':0}),
        }
        labels = {
            'producto': 'Producto',
            'cantidad': 'Cantidad',
        }