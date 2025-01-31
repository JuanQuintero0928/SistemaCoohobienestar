from django import forms
from .models import HistorialPagos, HistoricoSeguroVida, HistoricoAuxilio, HistoricoCredito
from parametro.models import TasasInteresCredito

# no se utiliza
class HistorialPagoForm(forms.ModelForm):
    class Meta:
        model = HistorialPagos
        fields = ['mesPago','formaPago','valorPago','aportePago','bSocialPago','mascotaPago','repatriacionPago','seguroVidaPago','coohopAporte','coohopBsocial','adicionalesPago']
        widgets = {
            'mesPago': forms.Select(
                attrs={
                    'class':'form-control',
                    'style':'text-transform: uppercase;',
                    # 'readonly':'readonly'
                }
            ),
            'formaPago': forms.Select(
                attrs={ 
                    'class':'form-control'
                }
            ),
            'valorPago': forms.NumberInput(
                attrs={
                    'class':'form-control',
                    'readonly':'readonly'
                }
            ),
            'aportePago': forms.NumberInput(
                attrs={ 
                    'class':'form-control',
                    'readonly':'readonly'
                }
            ),
            'bSocialPago': forms.NumberInput(
                attrs={ 
                    'class':'form-control',
                    'maxlength':'10',
                    'readonly':'readonly'
                }
            ),
            'mascotaPago': forms.NumberInput(
                attrs={
                    'class':'form-control',
                    'readonly':'readonly'
                }
            ),
            'repatriacionPago': forms.NumberInput(   
                attrs={
                    'class':'form-control',
                    'readonly':'readonly'
                }
            ),
            'seguroVidaPago': forms.NumberInput(
                attrs={ 
                    'class':'form-control',
                    'readonly':'readonly'
                }
            ),
            'coohopAporte': forms.NumberInput(
                attrs={ 
                    'class':'form-control',
                    'readonly':'readonly'
                }
            ),
            'coohopBsocial': forms.NumberInput(
                attrs={ 
                    'class':'form-control',
                    'readonly':'readonly'
                }
            ),
            'adicionalesPago': forms.NumberInput(
                attrs={ 
                    'class':'form-control',
                    'readonly':'readonly' 
                }
            ),
        }

class HistoricoSeguroVidaForm(forms.ModelForm):
    class Meta:
        model = HistoricoSeguroVida
        fields = ['valorPago','fechaIngreso', 'fechaRetiro']
        widgets = {
            'valorPago': forms.NumberInput(
                attrs={
                    'class':'form-control',
                }
            ),
            'fechaIngreso': forms.DateInput(
                attrs={ 
                    'class':'form-control',
                    'type':'date'
                }
            ),
            'fechaRetiro': forms.DateInput(
                attrs={ 
                    'class':'form-control',
                    'type':'date'
                }
            ),
        }

class HistoricoAuxilioForm(forms.ModelForm):
    class Meta:
        model = HistoricoAuxilio
        fields = ['fechaSolicitud','tipoAuxilio','entidadBancaria','numCuenta','estado']
        widgets = {
            'fechaSolicitud': forms.DateInput(
                attrs={ 
                    'class':'form-control',
                    'type':'date',
                    'required':'required'
                }
            ),
             'tipoAuxilio': forms.Select(
                attrs={ 
                    'class':'form-control',
                    'required':'required'
                }
            ),
            'estado': forms.Select(
                attrs={ 
                    'class':'form-control',
                    'required':'required'
                }
            ),
            'entidadBancaria': forms.TextInput(
                attrs={ 
                    'class':'form-control',
                    'style': 'text-transform: uppercase;',
                    'required':'required'
                }
            ),
            'numCuenta': forms.TextInput(
                attrs={
                    'class':'form-control',
                    'required':'required'
                }
            )
        }

class HistoricoCreditoForm(forms.ModelForm):

    tasaInteres = forms.ModelChoiceField(
        queryset=TasasInteresCredito.objects.all(),
        label="Tasa de interés mensual (%)",
        empty_label="Seleccione una tasa",
        widget=forms.Select(attrs={'class': 'form-select', 'id': 'tasaInteres'}),
        to_field_name="porcentaje"  # <-- Aquí se define que el value sea el porcentaje en vez del ID
    )

    class Meta:
        model = HistoricoCredito
        fields = ['fechaSolicitud',
                  'valor',
                  'cuotas',
                  'lineaCredito',
                  'amortizacion',
                  'medioPago',
                  'tasaInteres',
                  'formaDesembolso',
                  'valorCuota',
                  'totalCredito',
                  'estado'
                  ]
        labels = {
            'fechaSolicitud': 'Fecha Solicitud',
            'valor': 'Valor',
            'cuotas': 'Cuotas',
            'lineaCredito': 'Linea Crédito',
            'amortizacion': 'Amortización',
            'medioPago': 'Medio de Pago',
            'formaDesembolso': 'Forma de Desembolso',
            'estado': 'Estado'
        }
        widgets = {
            'fechaSolicitud': forms.DateInput(
                attrs={ 
                    'class':'form-control',
                    'type':'date',
                    'id':'fechaSolicitud',
                },format='%Y-%m-%d'
            ),
            'valor': forms.NumberInput(
                attrs={
                    'class':'form-control',
                    'min':'0',
                    'id':'valor'
                }
            ),
            'cuotas': forms.NumberInput(
                attrs={
                    'class':'form-control',
                    'min':'0',
                    'id':'cuotas'
                }
            ),
            'valorCuota': forms.NumberInput(
                attrs={
                    'class':'form-control',
                    # 'hidden':'hidden',
                }
            ),
            'totalCredito': forms.NumberInput(
                attrs={
                    'class':'form-control',
                    # 'hidden':'hidden',
                }
            ),
            'lineaCredito': forms.Select(
                attrs={ 
                    'class':'form-control'
                }
            ),
            'amortizacion': forms.Select(
                attrs={ 
                    'class':'form-control'
                }
            ),
            'medioPago': forms.Select(
                attrs={ 
                    'class':'form-control'
                }
            ),
            'formaDesembolso': forms.Select(
                attrs={ 
                    'class':'form-control'
                }
            ),
            'estado': forms.Select(
                attrs={ 
                    'class':'form-control'
                }
            ),
        }
    

class CargarArchivoForm(forms.Form):
    archivo_csv = forms.FileField(
        label="Seleccione un archivo CSV",
        widget=forms.ClearableFileInput(attrs={
            'class': 'form-control',  # Clase de Bootstrap o personalizada
            'accept': '.csv',  # Opcional: restringe a archivos CSV
        })
    )