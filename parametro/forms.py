from django import forms
from beneficiario.models import Parentesco
from departamento.models import PaisRepatriacion, Pais
from .models import Tarifas, TipoAsociado, TipoAuxilio, MesTarifa, Convenio, TasasInteresCredito

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

class MesTarifaForm(forms.ModelForm):
    class Meta:
        model = MesTarifa
        fields = ['concepto','aporte','bSocial','fechaInicio','fechaFinal']
        labels = {
            'concepto':'Concepto',
            'aporte':'Valor Aporte',
            'bSocial':'Valor Bienestar Social',
            'fechaInicio':'Fecha Inicial',
            'fechaFinal':'Fecha Final',
        }
        widgets = {
            'concepto' : forms.TextInput(
                attrs={
                    'class':'form-control',
                    'style':'text-transform: uppercase;',
                }
            ),
            'aporte': forms.NumberInput(
                attrs={
                    'class':'form-control',
                }
            ),
            'bSocial': forms.NumberInput(
                attrs={
                    'class':'form-control',
                }
            ),
            'fechaInicio': forms.DateInput(
                attrs={
                    'class':'form-control',
                    'type': 'date',
                },
                format='%Y-%m-%d'
            )
            ,'fechaFinal': forms.DateInput(
                attrs={
                    'class':'form-control',
                    'type': 'date',
                },
                format='%Y-%m-%d'
            ),
        }
    
    def clean_concepto(self):
        return self.cleaned_data['concepto'].upper()
    
class ConvenioForm(forms.ModelForm):
    class Meta:
        model = Convenio
        fields = ['concepto', 'valor', 'fechaInicio', 'fechaTerminacion']
        labels = {
            'concepto':'Nombre del Convenio',
            'valor':'Valor del Convenio',
            'fechaInicio':'Fecha Inicial',
            'fechaTerminacion':'Fecha Terminación',
        }
        widgets = {
            'concepto': forms.TextInput(
                attrs={
                    'class':'form-control',
                    'style':'text-transform: uppercase;',
                }
            ),
            'valor': forms.NumberInput(
                attrs={
                    'class':'form-control',
                }
            ),
            'fechaInicio': forms.DateInput(
                attrs={
                    'class':'form-control',
                    'type': 'date',
                },
                format='%Y-%m-%d'
            ),
            'fechaTerminacion': forms.DateInput(
                attrs={
                    'class':'form-control',
                    'type': 'date',
                },
                format='%Y-%m-%d'
            ),
        }

    def clean_concepto(self):
        return self.cleaned_data['concepto'].upper()
    
class TasasInteresCreditoForm(forms.ModelForm):
    class Meta:
        model = TasasInteresCredito
        fields = ['concepto', 'porcentaje']
        labels = {
            'concepto':'Concepto',
            'porcentaje':'Porcentaje',
        }
        widgets = {
            'concepto': forms.TextInput(
                attrs={
                    'class':'form-control',
                    'style':'text-transform: uppercase;',
                }
            ),
            'porcentaje': forms.NumberInput(
                attrs={
                    'class':'form-control',
                    'step':'0.0001',
                    'min':'0',
                    'placeholder':'0.0024',
                }
            ),
        }
    
    def clean_concepto(self):
        return self.cleaned_data['concepto'].upper()