from pyexpat import model
from django import forms
from .models import HistorialPagos, HistoricoSeguroVida, HistoricoAuxilio, HistoricoCredito

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

    class Meta:
        model = HistoricoCredito
        fields = ['fechaSolicitud','valor','cuotas','estado']
        widgets = {
            'fechaSolicitud': forms.DateInput(
                attrs={ 
                    'class':'form-control',
                    'type':'date',
                },format='%Y-%m-%d'
            ),
            'valor': forms.NumberInput(
                attrs={
                    'class':'form-control'
                }
            ),
            'cuotas': forms.NumberInput(
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

    from django import forms

class CargarArchivoForm(forms.Form):
    archivo_csv = forms.FileField(
        label="Seleccione un archivo CSV",
        widget=forms.ClearableFileInput(attrs={
            'class': 'form-control',  # Clase de Bootstrap o personalizada
            'accept': '.csv',  # Opcional: restringe a archivos CSV
        })
    )