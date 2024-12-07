from cProfile import label
from turtle import width
from django import forms
from .models import Asociado, RepatriacionTitular, ConveniosAsociado
# from parametro.models import ConvenioAsociado

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

class RepatriacionTitularForm(forms.ModelForm):
    class Meta:
        model = RepatriacionTitular
        fields = ['fechaRepatriacion','paisRepatriacion', 'ciudadRepatriacion']
        labels = {
            'fechaRepatriacion': 'Fecha Repatriación',
            'paisRepatriacion': 'Pais Repatriación',
            'ciudadRepatriacion': 'Ciudad Repatriación',
        }
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
            'ciudadRepatriacion': forms.TextInput(
                attrs={
                    'class':'form-control',
                    'style':'text-transform: uppercase;'
                }
            ),
        }

class ConvenioAsociadoForm(forms.ModelForm):
    class Meta:
        model = ConveniosAsociado
        fields = ['convenio','fechaIngreso']
        labels = {
            'convenio': 'Nombre del Convenio',
            'fechaIngreso': 'Fecha Ingreso',
        }
        widgets = {
            'convenio': forms.Select(
                attrs={
                    'class':'form-control',
                    'style':'text-transform: uppercase;'
                }
            ),
            'fechaIngreso': forms.DateInput(
                attrs={
                    'class':'form-control',
                    'type': 'date'
                },
                format='%Y-%m-%d'
            ),
        }