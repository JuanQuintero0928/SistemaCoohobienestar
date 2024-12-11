from cProfile import label
from dataclasses import field
from pyexpat import model
from tkinter import Widget
from django import forms
from .models import Producto

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
