from django import forms
from beneficiario.models import Parentesco
from departamento.models import PaisRepatriacion
from parametro.models import Tarifas

class PaisRepatriacionForm(forms.ModelForm):
    class Meta:
        model = PaisRepatriacion
        fields = ['nombre']
        labels = {
            'nombre':'Nombre Pais'
        }
        widgets = {
            'nombre': forms.TextInput(
                attrs={
                    'class':'form-control',
                    'style':'text-transform: uppercase;',
                }
            ),
        }
    
    def clean_nombre(self):
        return self.cleaned_data['nombre'].upper()
    
class ParentescoForm(forms.ModelForm):
    class Meta:
        model = Parentesco
        fields = ['nombre']
        labels = {
            'nombre':'Nombre Parentesco'
        }
        widgets = {
            'nombre': forms.TextInput(
                attrs={
                    'class':'form-control',
                    'style':'text-transform: uppercase;',
                }
            ),
        }
    
    def clean_nombre(self):
        return self.cleaned_data['nombre'].upper()
    
class TarifasForm(forms.ModelForm):
    class Meta:
        model = Tarifas
        fields = ['concepto', 'cuenta', 'valor']
        labels = {
            'concepto':'Concepto',
            'cuenta':'Cuenta',
            'valor':'Valor',
        }
        widgets = {
            'concepto': forms.TextInput(
                attrs={
                    'class':'form-control',
                    'style':'text-transform: uppercase;',
                }
            ),
            'cuenta': forms.TextInput(
                attrs={
                    'class':'form-control',
                    'style':'text-transform: uppercase;',
                }
            ),
            'valor': forms.NumberInput(
                attrs={
                    'class':'form-control',
                    'style':'text-transform: uppercase;',
                }
            ),
        }

    def clean_concepto(self):
        return self.cleaned_data['concepto'].upper()