from django import forms

from asociado import form
from .models import Beneficiario, Mascota, Coohoperativitos

class BeneficiarioForm(forms.ModelForm):
    class Meta:
        model = Beneficiario
        fields = ['nombre','apellido','tipoDocumento','numDocumento','fechaNacimiento','parentesco','paisRepatriacion','fechaRepatriacion','fechaIngreso']
        widgets = {
            'nombre': forms.TextInput(
                attrs={
                    'class':'form-control',
                    'style':'text-transform: uppercase;'
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
            'numDocumento': forms.NumberInput(
                attrs={ 
                    'class':'form-control',
                    'min':10
                }
            ),
            'fechaNacimiento': forms.DateInput(
                attrs={
                    'class':'form-control',
                    'type': 'date',
                },
                format='%Y-%m-%d'
            ),
            'parentesco': forms.Select(
                attrs={ 
                    'class':'form-control'
                }
            ),
            'paisRepatriacion': forms.Select(
                attrs={ 
                    'class':'form-control'
                }
            ),
            'fechaIngreso': forms.DateInput(
                attrs={ 
                    'class':'form-control',
                    'type': 'date'
                },
                format='%Y-%m-%d'
            ),
            'fechaRepatriacion': forms.DateInput(
                attrs={
                    'class': 'form-control',
                    'type': 'date',
                },
                format='%Y-%m-%d'
            )
        }

class MascotaForm(forms.ModelForm):
    class Meta:
        model = Mascota
        fields = ['nombre','tipo','raza','fechaNacimiento','vacunasCompletas','fechaIngreso']
        widgets = {
            'nombre': forms.TextInput(
                attrs={
                    'class':'form-control',
                    'style':'text-transform: uppercase;'
                }
            ),
            'tipo': forms.Select(
                attrs={
                    'class':'form-control',
                    'style':'text-transform: uppercase;'
                }
            ),
            'raza': forms.TextInput(
                attrs={ 
                    'class':'form-control',
                    'style':'text-transform: uppercase;'
                }
            ),
            'fechaNacimiento': forms.DateInput(
                attrs={
                    'class':'form-control',
                    'type': 'date'
                }
            ),
            'vacunasCompletas': forms.CheckboxInput(
                attrs={ 
                }
            ),
            'fechaIngreso': forms.DateInput(
                attrs={ 
                    'class':'form-control',
                    'type': 'date'
                }
            ),
        }

class CoohoperativitoForm(forms.ModelForm):
    class Meta:
        model = Coohoperativitos
        fields = ['nombre','apellido','tipoDocumento','numDocumento','fechaNacimiento','fechaIngreso']
        widgets = {
            'nombre': forms.TextInput(
                attrs={
                    'class':'form-control',
                    'style':'text-transform: uppercase;'
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
                    'type': 'number'
                }
            ),
            'fechaNacimiento': forms.DateInput(
                attrs={ 
                    'class':'form-control',
                    'type': 'date'
                }, format='%Y-%m-%d',
            ),
            'fechaIngreso': forms.DateInput(
                attrs={ 
                    'class':'form-control',
                    'type': 'date'
                },format='%Y-%m-%d',
            ),
        }