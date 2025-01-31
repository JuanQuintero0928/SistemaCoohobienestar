from django import forms
from departamento.models import Municipio
from .models import Codeudor

class CodeudorForm(forms.ModelForm):
    class Meta:
        model = Codeudor
        fields = ['nombre','apellido','tipoDocumento','numDocumento','fechaExpedicion','mpioDoc','nacionalidad','genero','estadoCivil','email','fechaNacimiento','dtoNacimiento','mpioNacimiento','tipoVivienda','estrato','direccion','barrio','deptoResidencia','mpioResidencia','numCelular', 'ingresosTotales', 'egresosTotales']
        widgets = {
            'nombre': forms.TextInput(attrs={'class':'form-control','style':'text-transform: uppercase;',}),
            'apellido': forms.TextInput(attrs={'class':'form-control','style':'text-transform: uppercase;',}),
            'tipoDocumento': forms.Select(attrs={'class':'form-control','style':'text-transform: uppercase;',}),
            'numDocumento': forms.NumberInput(attrs={'class':'form-control','maxlength':'11', 'min':'0',}),
            'fechaExpedicion': forms.DateInput(attrs={'class':'form-control','type': 'date',}, format='%Y-%m-%d'),
            'mpioDoc': forms.Select(attrs={'class':'form-control',}),
            'nacionalidad': forms.TextInput(attrs={'class':'form-control','style':'text-transform: uppercase;',}),
            'genero': forms.Select(attrs={'class':'form-control',}),
            'estadoCivil': forms.Select(attrs={'class':'form-control',}),
            'email': forms.EmailInput(attrs={'class':'form-control',}),
            'fechaNacimiento': forms.DateInput(attrs={'class':'form-control','type': 'date',}, format='%Y-%m-%d'),
            'dtoNacimiento': forms.Select(attrs={'class':'form-control',}),
            'mpioNacimiento': forms.Select(attrs={'class':'form-control',}),
            'tipoVivienda': forms.Select(attrs={'class':'form-control',}),
            'estrato': forms.NumberInput(attrs={'class':'form-control','min':'0',}),
            'direccion': forms.TextInput(attrs={'class':'form-control','style':'text-transform: uppercase;',}),
            'barrio': forms.TextInput(attrs={'class':'form-control','style':'text-transform: uppercase;',}),
            'deptoResidencia': forms.Select(attrs={'class':'form-control',}),
            'mpioResidencia': forms.Select(attrs={'class':'form-control',}),
            'numCelular': forms.NumberInput(attrs={'class':'form-control','min':'0',}),
            'ingresosTotales': forms.NumberInput(attrs={'class':'form-control','min':'0',}),
            'egresosTotales': forms.NumberInput(attrs={'class':'form-control','min':'0',}),
        }
        labels = {
            'nombre': 'Nombre',
            'apellido': 'Apellido',
            'tipoDocumento': 'Tipo Documento',
            'numDocumento': 'Número Documento',
            'fechaExpedicion': 'Fecha Expedición',
            'mpioDoc': 'Municipio de Expedición',
            'nacionalidad': 'Nacionalidad',
            'genero': 'Género',
            'estadoCivil': 'Estado Civil',
            'email': 'Email',
            'fechaNacimiento': 'Fecha Nacimiento',
            'dtoNacimiento': 'Departamento de Nacimiento',
            'mpioNacimiento': 'Municipio de Nacimiento',
            'tipoVivienda': 'Tipo de Vivienda',
            'estrato': 'Estrato',
            'direccion': 'Dirección',
            'barrio': 'Barrio',
            'deptoResidencia': 'Departamento de Residencia',
            'mpioResidencia': 'Municipio de Residencia',
            'numCelular': 'Número Celular',
            'ingresosTotales': 'Ingresos Mensuales',
            'egresosTotales': 'Egresos Mensuales',
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['mpioDoc'].queryset = Municipio.objects.select_related('departamento').all()
        self.fields['mpioDoc'].label_from_instance = lambda obj: f"{obj.departamento.nombre} - {obj.nombre}"