from django import forms
from .models import Empleados, Area, Cargo, TipoContrato, NombreUnidad, HistorialLaboral


class EmpleadoForm(forms.ModelForm):
    class Meta:
        model = Empleados
        fields = [
            "nombre",
            "apellido",
            "tipo_documento",
            "numero_documento",
            "fecha_nacimiento",
            "celular",
            "correo",
            "direccion",
            "departamento",
            "municipio",
        ]
        widgets = {
            "nombre": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Nombre del empleado",
                    "style": "text-transform: uppercase;",
                }
            ),
            "apellido": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Apellido del empleado",
                    "style": "text-transform: uppercase;",
                }
            ),
            "tipo_documento": forms.Select(attrs={"class": "form-control"}),
            "numero_documento": forms.NumberInput(
                attrs={"class": "form-control", "placeholder": "Número de documento"}
            ),
            "fecha_nacimiento": forms.DateInput(
                attrs={"class": "form-control", "type": "date"}, format="%Y-%m-%d"
            ),
            "celular": forms.NumberInput(
                attrs={"class": "form-control", "placeholder": "Número de celular"}
            ),
            "correo": forms.EmailInput(
                attrs={"class": "form-control", "placeholder": "Correo electrónico"}
            ),
            "direccion": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Dirección",
                    "style": "text-transform: uppercase;",
                }
            ),
            "departamento": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Departamento",
                    "style": "text-transform: uppercase;",
                }
            ),
            "municipio": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Municipio",
                    "style": "text-transform: uppercase;",
                }
            ),
        }


class AreaForm(forms.ModelForm):
    class Meta:
        model = Area
        fields = ["nombre"]
        widgets = {
            "nombre": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Nombre del área",
                    "style": "text-transform: uppercase;",
                }
            ),
        }


class CargoForm(forms.ModelForm):
    class Meta:
        model = Cargo
        fields = ["nombre"]
        widgets = {
            "nombre": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Nombre del cargo",
                    "style": "text-transform: uppercase;",
                }
            ),
        }


class TipoContratoForm(forms.ModelForm):
    class Meta:
        model = TipoContrato
        fields = ["nombre"]
        widgets = {
            "nombre": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Nombre del tipo de contrato",
                    "style": "text-transform: uppercase;",
                }
            ),
        }


class NombreUnidadForm(forms.ModelForm):
    class Meta:
        model = NombreUnidad
        fields = ["nombre"]
        widgets = {
            "nombre": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Nombre del la unidad de servicio",
                    "style": "text-transform: uppercase;",
                }
            ),
        }


class HistorialLaboralForm(forms.ModelForm):
    class Meta:
        model = HistorialLaboral
        fields = [
            "empleado",
            "area",
            "cargo",
            "tipo_contrato",
            "nombre_unidad",
            "fecha_inicio",
            "fecha_fin",
            "salario",
        ]
        widgets = {
            "empleado": forms.Select(attrs={"class": "form-control"}),
            "area": forms.Select(attrs={"class": "form-control"}),
            "cargo": forms.Select(attrs={"class": "form-control"}),
            "tipo_contrato": forms.Select(attrs={"class": "form-control"}),
            "nombre_unidad": forms.Select(attrs={"class": "form-control"}),
            "fecha_inicio": forms.DateInput(
                attrs={"class": "form-control", "type": "date"}, format="%Y-%m-%d"
            ),
            "fecha_fin": forms.DateInput(
                attrs={"class": "form-control", "type": "date"}, format="%Y-%m-%d"
            ),
            "salario": forms.NumberInput(
                attrs={"class": "form-control", "placeholder": "Salario del empleado"}
            ),
        }
