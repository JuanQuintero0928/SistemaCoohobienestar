from django import forms
from .models import (
    HistorialPagos,
    HistoricoSeguroVida,
    HistoricoAuxilio,
    HistoricoCredito,
)
from parametro.models import TasasInteresCredito, MesTarifa


# no se utiliza
class HistorialPagoForm(forms.ModelForm):
    class Meta:
        model = HistorialPagos
        fields = [
            "mesPago",
            "formaPago",
            "valorPago",
            "aportePago",
            "bSocialPago",
            "mascotaPago",
            "repatriacionPago",
            "seguroVidaPago",
            "coohopAporte",
            "coohopBsocial",
            "adicionalesPago",
        ]
        widgets = {
            "mesPago": forms.Select(
                attrs={
                    "class": "form-control",
                    "style": "text-transform: uppercase;",
                    # 'readonly':'readonly'
                }
            ),
            "formaPago": forms.Select(attrs={"class": "form-control"}),
            "valorPago": forms.NumberInput(
                attrs={"class": "form-control", "readonly": "readonly"}
            ),
            "aportePago": forms.NumberInput(
                attrs={"class": "form-control", "readonly": "readonly"}
            ),
            "bSocialPago": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "maxlength": "10",
                    "readonly": "readonly",
                }
            ),
            "mascotaPago": forms.NumberInput(
                attrs={"class": "form-control", "readonly": "readonly"}
            ),
            "repatriacionPago": forms.NumberInput(
                attrs={"class": "form-control", "readonly": "readonly"}
            ),
            "seguroVidaPago": forms.NumberInput(
                attrs={"class": "form-control", "readonly": "readonly"}
            ),
            "coohopAporte": forms.NumberInput(
                attrs={"class": "form-control", "readonly": "readonly"}
            ),
            "coohopBsocial": forms.NumberInput(
                attrs={"class": "form-control", "readonly": "readonly"}
            ),
            "adicionalesPago": forms.NumberInput(
                attrs={"class": "form-control", "readonly": "readonly"}
            ),
        }


class HistoricoSeguroVidaForm(forms.ModelForm):
    class Meta:
        model = HistoricoSeguroVida
        fields = ["valorPago", "fechaIngreso", "primerMesSeguroVida", "fechaRetiro"]
        labels = {
            "primerMesSeguroVida": "Primer mes de seguro de vida",
        }
        widgets = {
            "valorPago": forms.NumberInput(
                attrs={
                    "class": "form-control",
                }
            ),
            "fechaIngreso": forms.DateInput(
                attrs={"class": "form-control", "type": "date"},
                format="%Y-%m-%d",
            ),
            "primerMesSeguroVida": forms.Select(
                attrs={
                    "class": "form-control",
                    "style": "text-transform: uppercase;",
                    "required": "required",
                }
            ),
            "fechaRetiro": forms.DateInput(
                attrs={"class": "form-control", "type": "date"}
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

        self.fields["primerMesSeguroVida"].queryset = queryset


class HistoricoAuxilioForm(forms.ModelForm):
    class Meta:
        model = HistoricoAuxilio
        fields = [
            "fechaSolicitud",
            "tipoAuxilio",
            "entidadBancaria",
            "numCuenta",
            "estado",
        ]
        widgets = {
            "fechaSolicitud": forms.DateInput(
                attrs={"class": "form-control", "type": "date", "required": "required"}
            ),
            "tipoAuxilio": forms.Select(
                attrs={"class": "form-control", "required": "required"}
            ),
            "estado": forms.Select(
                attrs={"class": "form-control", "required": "required"}
            ),
            "entidadBancaria": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "style": "text-transform: uppercase;",
                }
            ),
            "numCuenta": forms.TextInput(
                attrs={
                    "class": "form-control",
                }
            ),
        }


class HistoricoCreditoForm(forms.ModelForm):

    tasaInteres = forms.ChoiceField(
        label="Tasa de interés mensual (%)",
        choices=[],
        widget=forms.Select(attrs={"class": "form-select", "id": "id_tasaInteres"})
    )

    class Meta:
        model = HistoricoCredito
        fields = [
            "fechaSolicitud",
            "valor",
            "cuotas",
            "lineaCredito",
            "amortizacion",
            "medioPago",
            "tasaInteres",
            "formaDesembolso",
            "valorCuota",
            "totalCredito",
            "estado",
            "banco",
            "primerMes",
            "numCuenta",
            "tipoCuenta",
        ]
        labels = {
            "fechaSolicitud": "Fecha Solicitud",
            "valor": "Valor",
            "cuotas": "Cuotas",
            "lineaCredito": "Linea Crédito",
            "amortizacion": "Amortización",
            "medioPago": "Medio de Pago",
            "formaDesembolso": "Forma de Desembolso",
            "estado": "Estado",
            "Banco": "Banco",
            "numCuenta": "Número de Cuenta",
            "Tipo Cuenta": "Tipo Cuenta",
            "primerMes": "Primer Mes Cobro",
        }
        widgets = {
            "fechaSolicitud": forms.DateInput(
                attrs={
                    "class": "form-control",
                    "type": "date",
                    "id": "fechaSolicitud",
                },
                format="%Y-%m-%d",
            ),
            "valor": forms.NumberInput(
                attrs={"class": "form-control", "min": "0", "id": "valor"}
            ),
            "cuotas": forms.NumberInput(
                attrs={"class": "form-control", "min": "0", "id": "cuotas"}
            ),
            "valorCuota": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    # 'hidden':'hidden',
                }
            ),
            "totalCredito": forms.NumberInput(
                attrs={
                    "class": "form-control",
                }
            ),
            "lineaCredito": forms.Select(attrs={"class": "form-control"}),
            "amortizacion": forms.Select(attrs={"class": "form-control"}),
            "medioPago": forms.Select(attrs={"class": "form-control"}),
            "formaDesembolso": forms.Select(attrs={"class": "form-control"}),
            "estado": forms.Select(attrs={"class": "form-control"}),
            "numCuenta": forms.NumberInput(
                attrs={
                    "class": "form-control",
                }
            ),
            "tipoCuenta": forms.Select(attrs={"class": "form-control"}),
            "banco": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "style": "text-transform: uppercase;",
                }
            ),
            "primerMes": forms.Select(
                attrs={
                    "class": "form-control",
                    "style": "text-transform: uppercase;",
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        asociado_id = kwargs.pop("asociado_id", None)
        super().__init__(*args, **kwargs)

        # === Filtro de primerMes ===
        queryset = MesTarifa.objects.filter(id__lt=9000)
        if asociado_id:
            from asociado.models import ParametroAsociado
            parametro = ParametroAsociado.objects.filter(asociado_id=asociado_id).first()
            if parametro and parametro.primerMes:
                queryset = queryset.filter(id__gte=parametro.primerMes.id)
        self.fields["primerMes"].queryset = queryset

        # === Construcción del select de tasas ===
        tasas = TasasInteresCredito.objects.all()
        self.fields["tasaInteres"].choices = [
            (f"{t.porcentaje}|{t.concepto}", t.concepto)
            for t in tasas
        ]
        self.fields["tasaInteres"].choices.insert(0, ("", "Seleccione una tasa"))

        # === Establecer valor inicial al editar ===
        if self.instance.pk and self.instance.tasaInteres:
            tasa = self.instance.tasaInteres
            self.initial["tasaInteres"] = f"{tasa.porcentaje}|{tasa.concepto}"

        # === Deshabilitar campos si el crédito ya fue otorgado ===
        NO_DESHABILITAR = ["estado", "primerMes"]

        if self.instance and getattr(self.instance, "estado", "").upper() == "OTORGADO":
            for name, field in self.fields.items():
                if name in NO_DESHABILITAR:
                    continue  # NO deshabilitar este campo
                field.disabled = True


class CargarArchivoForm(forms.Form):
    archivo_csv = forms.FileField(
        label="Seleccione un archivo CSV",
        widget=forms.ClearableFileInput(
            attrs={
                "class": "form-control",  # Clase de Bootstrap o personalizada
                "accept": ".csv",  # Opcional: restringe a archivos CSV
            }
        ),
    )
