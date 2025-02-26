from django import forms
from beneficiario.models import Parentesco
from departamento.models import PaisRepatriacion, Pais
from parametro.models import Tarifas, TipoAsociado, TipoAuxilio

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

class TipoAsociadoForm(forms.ModelForm):
    class Meta:
        model = TipoAsociado
        fields = ['concepto']
        labels = {
            'concepto':'Tipo Asociado'
        }
        widgets = {
            'concepto': forms.TextInput(
                attrs={
                    'class':'form-control',
                    'style':'text-transform: uppercase;',
                }
            ),
        }
    
    def clean_concepto(self):
        return self.cleaned_data['concepto'].upper()
    
class TipoAuxilioForm(forms.ModelForm):
    class Meta:
        model = TipoAuxilio
        fields = ['nombre', 'valor']
        labels = {
            'nombre':'Concepto',
            'valor':'Valor',
        }
        widgets = {
            'nombre': forms.TextInput(
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

    def clean_nombre(self):
        return self.cleaned_data['nombre'].upper()

class PaisForm(forms.ModelForm):
    class Meta:
        model = Pais
        fields = ['nombre','indicativo','bandera']
        labels = {
            'nombre':'Siglas Pais',
            'indicativo':'Indicativo Pais',
            'bandera':'Ruta Icono Pais',
        }
        widgets = {
            'nombre': forms.TextInput(
                attrs={
                    'class':'form-control',
                    'style':'text-transform: uppercase;',
                }
            ),
            'indicativo': forms.TextInput(
                attrs={
                    'class':'form-control',
                    'style':'text-transform: uppercase;',
                }
            ),
            'bandera': forms.TextInput(
                attrs={
                    'class':'form-control',
                    'style':'text-transform: lowercase;',
                }
            ),
        }

    def clean_nombre(self):
        return self.cleaned_data['nombre'].upper()
    
    def clean_bandera(self):
        return self.cleaned_data['bandera'].lower()