from django import forms
from .models import Asociado, RepatriacionTitular, ConveniosAsociado, TarifaAsociado
from parametro.models import MesTarifa


class AsociadoFormReadonly(forms.ModelForm):
    class Meta:
        model = Asociado
        fields = [
            "nombre",
            "apellido",
            "tipoDocumento",
            "numDocumento",
            "fechaExpedicion",
            "mpioDoc",
            "nacionalidad",
            "genero",
            "estadoCivil",
            "email",
            "numCelular",
            "fechaIngreso",
        ]
        widgets = {
            "nombre": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "style": "text-transform: uppercase;",
                    "disabled": "disabled",
                }
            ),
            "apellido": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "style": "text-transform: uppercase;",
                    "disabled": "disabled",
                }
            ),
            "tipoDocumento": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "style": "text-transform: uppercase;",
                    "disabled": "disabled",
                }
            ),
            "numDocumento": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "maxlength": "10",
                    "disabled": "disabled",
                }
            ),
            "fechaExpedicion": forms.DateInput(
                attrs={"class": "form-control", "type": "date", "disabled": "disabled"}
            ),
            "mpioDoc": forms.Select(
                attrs={"class": "form-control", "disabled": "disabled"}
            ),
            "nacionalidad": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "style": "text-transform: uppercase;",
                    "disabled": "disabled",
                }
            ),
            "genero": forms.TextInput(
                attrs={"class": "form-control", "disabled": "disabled"}
            ),
            "estadoCivil": forms.TextInput(
                attrs={"class": "form-control", "disabled": "disabled"}
            ),
            "email": forms.EmailInput(
                attrs={"class": "form-control", "disabled": "disabled"}
            ),
            "numCelular": forms.NumberInput(
                attrs={"class": "form-control", "disabled": "disabled"}
            ),
            "fechaIngreso": forms.DateInput(
                attrs={"class": "form-control", "type": "date", "disabled": "disabled"}
            ),
        }


class AsociadoForm(forms.ModelForm):
    class Meta:
        model = Asociado
        fields = [
            "nombre",
            "apellido",
            "tipoDocumento",
            "numDocumento",
            "fechaExpedicion",
            "mpioDoc",
            "nacionalidad",
            "genero",
            "estadoCivil",
            "email",
            "numCelular",
            "fechaIngreso",
        ]
        widgets = {
            "nombre": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "style": "text-transform: uppercase;",
                }
            ),
            "apellido": forms.TextInput(
                attrs={"class": "form-control", "style": "text-transform: uppercase;"}
            ),
            "tipoDocumento": forms.Select(
                attrs={"class": "form-control", "style": "text-transform: uppercase;"}
            ),
            "numDocumento": forms.TextInput(
                attrs={"class": "form-control", "maxlength": "10"}
            ),
            "fechaExpedicion": forms.DateInput(
                attrs={"class": "form-control", "type": "date"}
            ),
            "mpioDoc": forms.Select(attrs={"class": "form-control"}),
            "nacionalidad": forms.TextInput(
                attrs={"class": "form-control", "style": "text-transform: uppercase;"}
            ),
            "genero": forms.Select(attrs={"class": "form-control"}),
            "estadoCivil": forms.Select(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
            "numCelular": forms.NumberInput(attrs={"class": "form-control"}),
            "fechaIngreso": forms.DateInput(
                attrs={"class": "form-control", "type": "date"}
            ),
        }


class RepatriacionTitularForm(forms.ModelForm):
    class Meta:
        model = RepatriacionTitular
        fields = [
            "fechaRepatriacion",
            "paisRepatriacion",
            "ciudadRepatriacion",
            "primerMes",
        ]
        labels = {
            "fechaRepatriacion": "Fecha Repatriación",
            "paisRepatriacion": "Pais Repatriación",
            "ciudadRepatriacion": "Ciudad Repatriación",
            "primerMes": "Primer Mes",
        }
        widgets = {
            "fechaRepatriacion": forms.DateInput(
                attrs={"class": "form-control", "type": "date"},
                format="%Y-%m-%d",
            ),
            "paisRepatriacion": forms.Select(attrs={"class": "form-control"}),
            "ciudadRepatriacion": forms.TextInput(
                attrs={"class": "form-control", "style": "text-transform: uppercase;"}
            ),
            "primerMes": forms.Select(
                attrs={"class": "form-control", "style": "text-transform: uppercase;"}
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


class ConvenioAsociadoForm(forms.ModelForm):
    class Meta:
        model = ConveniosAsociado
        fields = ["convenio", "fechaIngreso", "primerMes"]
        labels = {
            "convenio": "Nombre del Convenio",
            "fechaIngreso": "Fecha Ingreso",
            "primerMes": "Primer mes de cobro",
        }
        widgets = {
            "convenio": forms.Select(
                attrs={"class": "form-control", "style": "text-transform: uppercase;"}
            ),
            "fechaIngreso": forms.DateInput(
                attrs={"class": "form-control", "type": "date"}, format="%Y-%m-%d"
            ),
            "primerMes": forms.Select(
                attrs={"class": "form-control", "style": "text-transform: uppercase;"}
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


class TarifaAsociadoAdicionalForm(forms.ModelForm):
    class Meta:
        model = TarifaAsociado
        fields = [
            "cuotaAdicionales",
            "fechaInicioAdicional",
            "conceptoAdicional",
            "primerMesCuotaAdicional",
        ]
        labels = {
            "cuotaAdicionales": "Valor Adicional",
            "fechaInicioAdicional": "Fecha Inicio Adicional",
            "conceptoAdicional": "Concepto Adicional",
            "primerMesCuotaAdicional": "Primer Mes",
        }
        widgets = {
            "cuotaAdicionales": forms.NumberInput(
                attrs={
                    "class": "form-control",
                }
            ),
            "conceptoAdicional": forms.TextInput(
                attrs={"class": "form-control", "style": "text-transform: uppercase;"}
            ),
            "fechaInicioAdicional": forms.DateInput(
                attrs={"class": "form-control", "type": "date"}, format="%Y-%m-%d"
            ),
            "primerMesCuotaAdicional": forms.Select(
                attrs={"class": "form-control", "style": "text-transform: uppercase;"}
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

        self.fields["primerMesCuotaAdicional"].queryset = queryset
