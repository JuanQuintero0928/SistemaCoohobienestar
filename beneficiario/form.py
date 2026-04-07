from django import forms
from .models import Beneficiario, Mascota, Coohoperativitos
from parametro.models import MesTarifa


class BeneficiarioForm(forms.ModelForm):

    repatriacion = forms.BooleanField(
        required=False,
        label="Activar repatriación",
        widget=forms.CheckboxInput(
            attrs={"class": "form-check-input", "role": "switch"}
        ),
    )

    class Meta:
        model = Beneficiario
        fields = [
            "nombre",
            "apellido",
            "tipoDocumento",
            "numDocumento",
            "fechaNacimiento",
            "parentesco",
            "fechaIngreso",
            "repatriacion",
            "paisRepatriacion",
            "fechaRepatriacion",
            "ciudadRepatriacion",
            "primerMesRepatriacion",
            "fechaRetiroRepatriacion",
            "ultimoMesRepatriacion",
        ]
        labels = {
            "paisRepatriacion": "Pais Repatriación",
            "primerMesRepatriacion": "Primer Mes Repatriación Cobro",
            "fechaRetiroRepatriacion": "Fecha Retiro Repatriación",
            "ultimoMesRepatriacion": "Ultimo Mes Repatriación Cobro",
        }
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
            "primerMesRepatriacion": forms.Select(
                attrs={
                    "class": "form-control",
                }
            ),
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
            "fechaRetiroRepatriacion": forms.DateInput(
                attrs={"class": "form-control", "type": "date"}, format="%Y-%m-%d"
            ),
            "ultimoMesRepatriacion": forms.Select(
                attrs={
                    "class": "form-control",
                }
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

        if self.instance and self.instance.primerMesRepatriacion:
            self.fields["ultimoMesRepatriacion"].queryset = queryset.filter(
                id__gte=self.instance.primerMesRepatriacion.id
            )
        else:
            self.fields["ultimoMesRepatriacion"].queryset = queryset


class MascotaForm(forms.ModelForm):

    vacunasCompletas = forms.BooleanField(
        required=False,
        label="¿Tiene Vacunas Completas?",
        widget=forms.CheckboxInput(
            attrs={"class": "form-check-input", "role": "switch"}
        ),
    )

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


class RetiroMascotaForm(forms.ModelForm):
    class Meta:
        model = Mascota
        fields = ["fechaRetiro", "ultimoMes"]
        labels = {
            "fechaRetiro": "Fecha Retiro",
            "ultimoMes": "Último Mes Cobro",
        }
        widgets = {
            "fechaRetiro": forms.DateInput(
                attrs={"type": "date", "class": "form-control"}, format="%Y-%m-%d"
            ),
            "ultimoMes": forms.Select(attrs={"class": "form-control js-ultimo-mes"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # obligatorios
        self.fields["fechaRetiro"].required = True
        self.fields["ultimoMes"].required = True

        # limitar meses según primerMes
        if self.instance and self.instance.primerMes:
            self.fields["ultimoMes"].queryset = MesTarifa.objects.filter(
                pk__gte=self.instance.primerMes.pk
            ).exclude(pk__gt=9000)


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
            "primerMes",
            "ultimoMes",
        ]
        labels = {
            "primerMes": "Primer Mes Cobro",
            "ultimoMes": "Último Mes Cobro",
        }

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
            "primerMes": forms.Select(
                attrs={"class": "form-control", "required": "required"}
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["fechaNacimiento"].required = True

        # Filtrar choices
        self.fields['tipoDocumento'].choices = [
            choice for choice in self.fields['tipoDocumento'].choices
            if choice[0] not in ['CEDULA', 'CEDULA EXTRANJERA']
        ]

        asociado_id = kwargs.pop("asociado_id", None)

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

        if self.instance and self.instance.primerMes:
            self.fields["ultimoMes"].queryset = queryset.filter(
                id__gte=self.instance.primerMes.id
            )
        else:
            self.fields["ultimoMes"].queryset = queryset


class RetiroCoohoperativitoForm(forms.ModelForm):
    class Meta:
        model = Coohoperativitos
        fields = ["fechaRetiro", "ultimoMes"]
        labels = {
            "fechaRetiro": "Fecha Retiro",
            "ultimoMes": "Último Mes Cobro",
        }
        widgets = {
            "fechaRetiro": forms.DateInput(
                attrs={"type": "date", "class": "form-control"}, format="%Y-%m-%d"
            ),
            "ultimoMes": forms.Select(attrs={"class": "form-control js-ultimo-mes"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # obligatorios
        self.fields["fechaRetiro"].required = True
        self.fields["ultimoMes"].required = True

        # limitar meses según primerMes
        if self.instance and self.instance.primerMes:
            self.fields["ultimoMes"].queryset = MesTarifa.objects.filter(
                pk__gte=self.instance.primerMes.pk
            ).exclude(pk__gt=9000)