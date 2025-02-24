from django import forms
from departamento.models import PaisRepatriacion
# from parametro.models import ConvenioAsociado

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