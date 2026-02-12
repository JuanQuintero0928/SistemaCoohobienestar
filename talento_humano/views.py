from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q, Value, F
from django.db.models.functions import Concat
from django.core.paginator import Paginator
from django.urls import reverse_lazy
from django.contrib import messages

from django.views.generic import (
    CreateView,
    UpdateView,
    ListView,
    DeleteView,
    TemplateView,
)
from django.http import JsonResponse

from funciones.function import StaffRequiredMixin
from talento_humano.models import (
    Empleados,
    Area,
    Cargo,
    TipoContrato,
    NombreUnidad,
    HistorialLaboral,
)
from talento_humano.form import (
    EmpleadoForm,
    AreaForm,
    CargoForm,
    TipoContratoForm,
    NombreUnidadForm,
    HistorialLaboralForm,
)
from asociado.models import Asociado


class EmpleadoListView(LoginRequiredMixin, StaffRequiredMixin, ListView):
    model = Empleados
    template_name = "talento_humano/listar_empleados.html"
    context_object_name = "empleados"

    def get(self, request, *args, **kwargs):
        # Si es una petición AJAX, devolver JSON con paginación

        if request.headers.get("x-requested-with") == "XMLHttpRequest":
            start = int(request.GET.get("start", 0))
            length = int(request.GET.get("length", 10))
            search_value = request.GET.get("search_value", "").strip()

            # Obtener columna y dirección de ordenación
            order_column_index = int(request.GET.get("order[0][column]", 0))
            order_direction = request.GET.get("order[0][dir]", "asc")

            # Mapeo de columnas para ordenación
            column_map = [
                "id",
                "nombre",
                "apellido",
                "numero_documento",
                "celular",
            ]

            # Obtener columna de ordenación (por defecto 'id')
            order_column = (
                column_map[order_column_index]
                if order_column_index < len(column_map)
                else "id"
            )

            # Aplicar orden ascendente o descendente
            if order_direction == "desc":
                order_column = f"-{order_column}"

            # Obtener datos ordenados
            query = (
                Empleados.objects.annotate(
                    nombre_completo=Concat(F("nombre"), Value(" "), F("apellido"))
                )
                .values(
                    "id",
                    "nombre_completo",
                    "numero_documento",
                    "celular",
                )
                .order_by(order_column)
            )

            # Aplicar filtro de búsqueda
            if search_value:
                query = query.filter(
                    Q(id__icontains=search_value)
                    | Q(nombre__icontains=search_value)
                    | Q(apellido__icontains=search_value)
                    | Q(nombre_completo__icontains=search_value)
                    | Q(numero_documento__icontains=search_value)
                    | Q(celular__icontains=search_value)
                )

            total_records = query.count()

            # Aplicar paginación
            paginator = Paginator(query, length)
            page_number = (start // length) + 1
            page = paginator.get_page(page_number)

            return JsonResponse(
                {
                    "data": list(page),
                    "recordsTotal": total_records,
                    "recordsFiltered": total_records,
                }
            )

        else:
            # Renderizar la plantilla en la primera carga
            return render(request, self.template_name)


class EmpleadoCreateView(LoginRequiredMixin, StaffRequiredMixin, CreateView):
    model = Empleados
    form_class = EmpleadoForm
    template_name = "talento_humano/crear_empleado.html"
    success_url = reverse_lazy("talento_humano:listarEmpleados")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["operation"] = "crear"
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Empleado creado exitosamente.")
        asociado = form.cleaned_data.get("asociado") or ''
        if asociado:
            messages.info(
                self.request,
                f"El empleado esta ahora relacionado con el asociado ID{asociado.id} - {asociado.nombre} {asociado.apellido}.",
            )
            
        return response


class EmpleadoUpdateView(LoginRequiredMixin, StaffRequiredMixin, UpdateView):
    model = Empleados
    form_class = EmpleadoForm
    template_name = "talento_humano/crear_empleado.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["empleado"] = self.get_object()
        context["operation"] = "editar"
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Empleado actualizado exitosamente.")
        return response
    
    def get_success_url(self):
        return reverse_lazy(
            "talento_humano:editarEmpleado",
            kwargs={"pk": self.object.pk},
        )


class AreaListView(LoginRequiredMixin, StaffRequiredMixin, ListView):
    model = Area
    template_name = "talento_humano/listar_areas.html"
    context_object_name = "query"


class AreaCreateView(LoginRequiredMixin, StaffRequiredMixin, CreateView):
    model = Area
    form_class = AreaForm
    template_name = "talento_humano/crear_area.html"
    success_url = reverse_lazy("talento_humano:listarAreas")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["operation"] = "crear"
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Área creada exitosamente.")
        return response


class AreaUpdateView(LoginRequiredMixin, StaffRequiredMixin, UpdateView):
    model = Area
    form_class = AreaForm
    template_name = "talento_humano/crear_area.html"
    success_url = reverse_lazy("talento_humano:listarAreas")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["operation"] = "editar"
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Área actualizada exitosamente.")
        return response


class CargoListView(LoginRequiredMixin, StaffRequiredMixin, ListView):
    model = Cargo
    template_name = "talento_humano/listar_cargos.html"
    context_object_name = "query"


class CargoCreateView(LoginRequiredMixin, StaffRequiredMixin, CreateView):
    model = Cargo
    form_class = CargoForm
    template_name = "talento_humano/crear_cargo.html"
    success_url = reverse_lazy("talento_humano:listarCargos")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["operation"] = "crear"
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Cargo creado exitosamente.")
        return response


class CargoUpdateView(LoginRequiredMixin, StaffRequiredMixin, UpdateView):
    model = Cargo
    form_class = CargoForm
    template_name = "talento_humano/crear_cargo.html"
    success_url = reverse_lazy("talento_humano:listarCargos")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["operation"] = "editar"
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Cargo actualizado exitosamente.")
        return response


class NombreUnidadListView(LoginRequiredMixin, StaffRequiredMixin, ListView):
    model = NombreUnidad
    template_name = "talento_humano/listar_nombre_unidad.html"
    context_object_name = "query"


class NombreUnidadCreateView(LoginRequiredMixin, StaffRequiredMixin, CreateView):
    model = NombreUnidad
    form_class = NombreUnidadForm
    template_name = "talento_humano/crear_nombre_unidad.html"
    success_url = reverse_lazy("talento_humano:listarNombreUnidades")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["operation"] = "crear"
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Nombre de unidad creado exitosamente.")
        return response


class NombreUnidadUpdateView(LoginRequiredMixin, StaffRequiredMixin, UpdateView):
    model = NombreUnidad
    form_class = NombreUnidadForm
    template_name = "talento_humano/crear_nombre_unidad.html"
    success_url = reverse_lazy("talento_humano:listarNombreUnidades")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["operation"] = "editar"
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Nombre de unidad actualizado exitosamente.")
        return response


class TipoContratoListView(LoginRequiredMixin, StaffRequiredMixin, ListView):
    model = TipoContrato
    template_name = "talento_humano/listar_tipo_contrato.html"
    context_object_name = "query"


class TipoContratoCreateView(LoginRequiredMixin, StaffRequiredMixin, CreateView):
    model = TipoContrato
    form_class = TipoContratoForm
    template_name = "talento_humano/crear_tipo_contrato.html"
    success_url = reverse_lazy("talento_humano:listarTiposContrato")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["operation"] = "crear"
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Tipo de contrato creado exitosamente.")
        return response


class TipoContratoUpdateView(LoginRequiredMixin, StaffRequiredMixin, UpdateView):
    model = TipoContrato
    form_class = TipoContratoForm
    template_name = "talento_humano/crear_tipo_contrato.html"
    success_url = reverse_lazy("talento_humano:listarTiposContrato")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["operation"] = "editar"
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Tipo de contrato actualizado exitosamente.")
        return response


class HistorialLaboralListView(LoginRequiredMixin, StaffRequiredMixin, ListView):
    model = HistorialLaboral
    template_name = "talento_humano/listar_historial_laboral.html"
    context_object_name = "query"

    def get_queryset(self):
        self.empleado = get_object_or_404(Empleados, pk=self.kwargs["pk"])
        return HistorialLaboral.objects.filter(empleado=self.empleado).order_by(
            "-fecha_inicio"
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["empleado"] = self.empleado
        return context


class HistorialLaboralCreateView(LoginRequiredMixin, StaffRequiredMixin, CreateView):
    model = HistorialLaboral
    form_class = HistorialLaboralForm
    template_name = "talento_humano/crear_historial_laboral.html"

    def get_success_url(self):
        return reverse_lazy(
            "talento_humano:empleadolistarHistorialLaboral",
            kwargs={"pk": self.object.empleado.pk},
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["operation"] = "crear"
        context["empleado"] = get_object_or_404(Empleados, pk=self.kwargs["pk"])
        return context

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        empleado = get_object_or_404(Empleados, pk=self.kwargs["pk"])
        form.fields["empleado"].initial = empleado
        form.fields["empleado"].disabled = True
        return form

    def form_valid(self, form):
        empleado = get_object_or_404(Empleados, pk=self.kwargs["pk"])
        form.instance.empleado = empleado
        response = super().form_valid(form)
        messages.success(self.request, "Historial laboral creado exitosamente.")
        return response


class HistorialLaboralUpdateView(LoginRequiredMixin, StaffRequiredMixin, UpdateView):
    model = HistorialLaboral
    form_class = HistorialLaboralForm
    template_name = "talento_humano/crear_historial_laboral.html"

    def get_success_url(self):
        return reverse_lazy(
            "talento_humano:empleadolistarHistorialLaboral",
            kwargs={"pk": self.object.empleado.pk},
        )

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields["empleado"].disabled = True
        return form

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["operation"] = "editar"
        context["empleado"] = self.object.empleado
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Historial laboral actualizado exitosamente.")
        return response


class EliminarHistorialLaboral(DeleteView):
    model = HistorialLaboral
    template_name = "talento_humano/eliminar.html"

    def get_success_url(self):
        return reverse_lazy(
            "talento_humano:empleadolistarHistorialLaboral",
            kwargs={"pk": self.object.empleado.pk},
        )

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Historial laboral eliminado exitosamente.")
        return response


class UtilidadesProductos(TemplateView):
    template_name = "talento_humano/utilidades_empleado.html"


def buscar_persona_por_documento(request):
    numero = request.GET.get('numero_documento')

    try:
        persona = Asociado.objects.get(numDocumento=numero)
        return JsonResponse({
            'existe': True,
            'id_asociado': persona.id,
            'nombre': persona.nombre,
            'apellido': persona.apellido,
            'celular': persona.numCelular,
            'correo': persona.email,
            'direccion': persona.direccion,
            'fecha_nacimiento': persona.fechaNacimiento.strftime('%Y-%m-%d') if persona.fechaNacimiento else '',
            'municipio': persona.mpioResidencia.nombre if persona.mpioResidencia else '',
            'departamento': persona.deptoResidencia.nombre if persona.deptoResidencia else '',
        })
    except Asociado.DoesNotExist:
        return JsonResponse({'existe': False})