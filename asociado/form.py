from django import forms
from .models import Asociado, Residencia, RepatriacionTitular

class AsociadoFormReadonly(forms.ModelForm):
    class Meta:
        model = Asociado
        fields = ['nombre','apellido','tipoDocumento','numDocumento','fechaExpedicion','mpioDoc','nacionalidad','genero','estadoCivil','email','numCelular','fechaIngreso']
        widgets = {
            'nombre': forms.TextInput(
                attrs={
                    'class':'form-control',
                    'style':'text-transform: uppercase;',
                    'disabled':'disabled'
                }
            ),
            'apellido': forms.TextInput(
                attrs={
                    'class':'form-control',
                    'style':'text-transform: uppercase;',
                    'disabled':'disabled'
                }
            ),
            'tipoDocumento': forms.TextInput(
                attrs={ 
                    'class':'form-control',
                    'style':'text-transform: uppercase;',
                    'disabled':'disabled'
                }
            ),
            'numDocumento': forms.TextInput(
                attrs={ 
                    'class':'form-control',
                    'maxlength':'10',
                    'disabled':'disabled'
                }
            ),
            'fechaExpedicion': forms.DateInput(
                attrs={
                    'class':'form-control',
                    'type': 'date',
                    'disabled':'disabled'
                }
            ),
            'mpioDoc': forms.Select(   
                attrs={
                    'class':'form-control',
                    'disabled':'disabled'
                }
            ),
            'nacionalidad': forms.TextInput(
                attrs={ 
                    'class':'form-control',
                    'style':'text-transform: uppercase;',
                    'disabled':'disabled'
                }
            ),
            'genero': forms.TextInput(
                attrs={ 
                    'class':'form-control',
                    'disabled':'disabled'
                }
            ),
            'estadoCivil': forms.TextInput(
                attrs={ 
                    'class':'form-control',
                    'disabled':'disabled'
                }
            ),
            'email': forms.EmailInput(
                attrs={ 
                    'class':'form-control',
                    'disabled':'disabled'
                }
            ),
            'numCelular': forms.NumberInput(
                attrs={ 
                    'class':'form-control',
                    'disabled':'disabled'
                }
            ),
            'fechaIngreso': forms.DateInput(
                attrs={ 
                    'class':'form-control',
                    'type': 'date',
                    'disabled':'disabled'
                }
            ),
        }

class AsociadoForm(forms.ModelForm):
    class Meta:
        model = Asociado
        fields = ['nombre','apellido','tipoDocumento','numDocumento','fechaExpedicion','mpioDoc','nacionalidad','genero','estadoCivil','email','numCelular','fechaIngreso']
        widgets = {
            'nombre': forms.TextInput(
                attrs={
                    'class':'form-control',
                    'style':'text-transform: uppercase;',
                }
            ),
            'apellido': forms.TextInput(
                attrs={
                    'class':'form-control',
                    'style':'text-transform: uppercase;'
                }
            ),
            'tipoDocumento': forms.Select(
                attrs={ 
                    'class':'form-control',
                    'style':'text-transform: uppercase;'
                }
            ),
            'numDocumento': forms.TextInput(
                attrs={ 
                    'class':'form-control',
                    'maxlength':'10'
                }
            ),
            'fechaExpedicion': forms.DateInput(
                attrs={
                    'class':'form-control',
                    'type': 'date'
                }
            ),
            'mpioDoc': forms.Select(
                attrs={ 
                    'class':'form-control'
                }
            ),
            'nacionalidad': forms.TextInput(
                attrs={ 
                    'class':'form-control',
                    'style':'text-transform: uppercase;'
                }
            ),
            'genero': forms.Select(
                attrs={ 
                    'class':'form-control'
                }
            ),
            'estadoCivil': forms.Select(
                attrs={ 
                    'class':'form-control'
                }
            ),
            'email': forms.EmailInput(
                attrs={ 
                    'class':'form-control'
                }
            ),
            'numCelular': forms.NumberInput(
                attrs={ 
                    'class':'form-control'
                }
            ),
            'fechaIngreso': forms.DateInput(
                attrs={ 
                    'class':'form-control',
                    'type': 'date'
                }
            ),
        }

class ResidenciaFormReadonly(forms.ModelForm):
    class Meta:
        model = Residencia
        fields = ['tipoVivienda','estrato','direccion','barrio','deptoResidencia','mpioResidencia']
        widgets = {
            'tipoVivienda': forms.Select(
                attrs={ 
                    'class':'form-control',
                    'disabled':'disabled'
                }
            ),
            'estrato': forms.NumberInput(
                attrs={ 
                    'class':'form-control',
                    'disabled':'disabled'
                }
            ),
            'direccion': forms.TextInput(
                attrs={ 
                    'class':'form-control',
                    'disabled':'disabled'
                }
            ),
            'barrio': forms.TextInput(
                attrs={ 
                    'class':'form-control',
                    'disabled':'disabled'
                }
            ),
            'deptoResidencia': forms.Select(
                attrs={ 
                    'class':'form-control',
                    'disabled':'disabled'
                }
            ),
            'mpioResidencia': forms.Select(
                attrs={ 
                    'class':'form-control',
                    'disabled':'disabled'
                }
            ),
        }

class ResidenciaForm(forms.ModelForm):
    class Meta:
        model = Residencia
        fields = ['tipoVivienda','estrato','direccion','barrio','deptoResidencia','mpioResidencia']
        widgets = {
            'tipoVivienda': forms.Select(
                attrs={ 
                    'class':'form-control'
                }
            ),
            'estrato': forms.NumberInput(
                attrs={ 
                    'class':'form-control'
                }
            ),
            'direccion': forms.TextInput(
                attrs={ 
                    'class':'form-control'
                }
            ),
            'barrio': forms.TextInput(
                attrs={ 
                    'class':'form-control'
                }
            ),
            'deptoResidencia': forms.Select(
                attrs={ 
                    'class':'form-control'
                }
            ),
            'mpioResidencia': forms.Select(
                attrs={ 
                    'class':'form-control'
                }
            ),
        }

class RepatriacionTitularForm(forms.ModelForm):
    class Meta:
        model = RepatriacionTitular
        fields = ['fechaRepatriacion','paisRepatriacion']
        widgets = {
            'fechaRepatriacion': forms.DateInput(
                attrs={
                    'class':'form-control',
                    'type': 'date'
                },
                format='%Y-%m-%d',
            ),
            'paisRepatriacion': forms.Select(
                attrs={ 
                    'class':'form-control'
                }
            ),
        }