from django import forms

from asociado import form
from .models import Beneficiario, Mascota, Coohoperativitos
from parametro.models import MesTarifa


class BeneficiarioForm(forms.ModelForm):
    class Meta:
        model = Beneficiario
        fields = [
            "nombre",
            "apellido",
            "tipoDocumento",
            "numDocumento",
            "fechaNacimiento",
            "parentesco",
            "paisRepatriacion",
            "fechaRepatriacion",
            "primerMesRepatriacion",
            "ciudadRepatriacion",
            "fechaIngreso",
        ]
        widgets = {
            "nombre": forms.TextInput(
                attrs={"class": "form-control", "style": "text-transform: uppercase;"}
            ),
            "apellido": forms.TextInput(
                attrs={"class": "form-control", "style": "text-transform: uppercase;"}
            ),
            "tipoDocumento": forms.Select(
                attrs={"class": "form-control", "style": "text-transform: uppercase;"}
            ),
            "numDocumento": forms.NumberInput(
                attrs={"class": "form-control", "min": 10}
            ),
            "fechaNacimiento": forms.DateInput(
                attrs={
                    "class": "form-control",
                    "type": "date",
                },
                format="%Y-%m-%d",
            ),
            "parentesco": forms.Select(attrs={"class": "form-control"}),
            "paisRepatriacion": forms.Select(attrs={"class": "form-control"}),
            "fechaIngreso": forms.DateInput(
                attrs={"class": "form-control", "type": "date"}, format="%Y-%m-%d"
            ),
            "primerMesRepatriacion": forms.Select(attrs={"class": "form-control"}),
            "fechaRepatriacion": forms.DateInput(
                attrs={
                    "class": "form-control",
                    "type": "date",
                },
                format="%Y-%m-%d",
            ),
            "ciudadRepatriacion": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "type": "text",
                    "style": "text-transform: uppercase;",
                },
            ),
        }

    def __init__(self, *args, **kwargs):
        # id del asociado desde la vista
        asociado_id = kwargs.pop("asociado_id", None)
        super().__init__(*args, **kwargs)

        # Filtro base
        queryset = MesTarifa.objects.filter(id__lt=9000)

        # Si tenemos el asociado, filtramos por el primer mes
        if asociado_id:
            from asociado.models import ParametroAsociado

            parametro = ParametroAsociado.objects.filter(
                asociado_id=asociado_id
            ).first()
            if parametro and parametro.primerMes:
                # Filtra solo los meses posteriores al primerMes del asociado
                queryset = queryset.filter(id__gte=parametro.primerMes.id)

        self.fields["primerMesRepatriacion"].queryset = queryset


class MascotaForm(forms.ModelForm):
    class Meta:
        model = Mascota
        fields = [
            "nombre",
            "tipo",
            "raza",
            "fechaNacimiento",
            "vacunasCompletas",
            "fechaIngreso",
            "primerMes",
        ]
        widgets = {
            "nombre": forms.TextInput(
                attrs={"class": "form-control", "style": "text-transform: uppercase;"}
            ),
            "tipo": forms.Select(
                attrs={"class": "form-control", "style": "text-transform: uppercase;"}
            ),
            "raza": forms.TextInput(
                attrs={"class": "form-control", "style": "text-transform: uppercase;"}
            ),
            "fechaNacimiento": forms.DateInput(
                attrs={"class": "form-control", "type": "date"},
                format="%Y-%m-%d",
            ),
            "vacunasCompletas": forms.CheckboxInput(attrs={}),
            "fechaIngreso": forms.DateInput(
                attrs={"class": "form-control", "type": "date"},
                format="%Y-%m-%d",
            ),
            "primerMes": forms.Select(
                attrs={"class": "form-control", "required": "required"}
            ),
        }

    def __init__(self, *args, **kwargs):
        # id del asociado desde la vista
        asociado_id = kwargs.pop("asociado_id", None)
        super().__init__(*args, **kwargs)

        # Filtro base
        queryset = MesTarifa.objects.filter(id__lt=9000)

        # Si tenemos el asociado, filtramos por el primer mes
        if asociado_id:
            from asociado.models import ParametroAsociado

            parametro = ParametroAsociado.objects.filter(
                asociado_id=asociado_id
            ).first()
            if parametro and parametro.primerMes:
                # Filtra solo los meses posteriores al primerMes del asociado
                queryset = queryset.filter(id__gte=parametro.primerMes.id)

        self.fields["primerMes"].queryset = queryset


class CoohoperativitoForm(forms.ModelForm):
    class Meta:
        model = Coohoperativitos
        fields = [
            "nombre",
            "apellido",
            "tipoDocumento",
            "numDocumento",
            "fechaNacimiento",
            "fechaIngreso",
        ]
        widgets = {
            "nombre": forms.TextInput(
                attrs={"class": "form-control", "style": "text-transform: uppercase;"}
            ),
            "apellido": forms.TextInput(
                attrs={"class": "form-control", "style": "text-transform: uppercase;"}
            ),
            "tipoDocumento": forms.Select(
                attrs={"class": "form-control", "style": "text-transform: uppercase;"}
            ),
            "numDocumento": forms.TextInput(
                attrs={"class": "form-control", "type": "number"}
            ),
            "fechaNacimiento": forms.DateInput(
                attrs={"class": "form-control", "type": "date"},
                format="%Y-%m-%d",
            ),
            "fechaIngreso": forms.DateInput(
                attrs={"class": "form-control", "type": "date"},
                format="%Y-%m-%d",
            ),
        }
