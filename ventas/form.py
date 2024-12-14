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
                  'descuento',
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
            'descuento': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '0.20', 'min': 0, 'max': 1}),
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
            'descuento': 'Descuento (%)',
            'proveedor': 'Proveedor',
            'stock': 'Stock disponible'
        }

class HistoricoVentaForm(forms.ModelForm):
    class Meta:
        model = HistoricoVenta
        fields = ['fechaVenta',
                  'formaPago',
                  'cuotas',
                  'valorBruto',
                  'valorNeto',
        ]
        widgets = {
            'fechaVenta': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'},format='%Y-%m-%d',),
            'formaPago': forms.Select(attrs={'class': 'form-control'}),
            'cuotas': forms.NumberInput(attrs={'class': 'form-control', 'min':0}),
            'valorBruto': forms.NumberInput(attrs={'class': 'form-control', 'readonly':'readonly'}),
            'valorNeto': forms.NumberInput(attrs={'class': 'form-control', 'readonly':'readonly'}),
        }
        labels = {
            'fechaVenta': 'Fecha Venta',
            'formaPago': 'Forma Pago',
            'cuotas': 'Número Cuotas',
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