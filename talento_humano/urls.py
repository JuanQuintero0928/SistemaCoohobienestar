from django.urls import path
from django.contrib.auth.decorators import login_required
from .views import *

urlpatterns = [
    path('listar-empleados/', login_required(EmpleadoListView.as_view()), name='listarEmpleados'),
    path('crear-empleado/', login_required(EmpleadoCreateView.as_view()), name='crearEmpleado'),
    path('ver-empleado/<int:pk>/', login_required(EmpleadoUpdateView.as_view()), name='editarEmpleado'),
    path('empleado-historial-laboral/<int:pk>/', login_required(HistorialLaboralListView.as_view()), name='empleadolistarHistorialLaboral'),
    path('crear-historial-laboral/<int:pk>/', login_required(HistorialLaboralCreateView.as_view()), name='empleadocrearHistorialLaboral'),
    path('editar-historial-laboral/<int:pk>/', login_required(HistorialLaboralUpdateView.as_view()), name='empleadoeditarHistorialLaboral'),
    path('historial-laboral/<int:pk>/eliminar/', login_required(EliminarHistorialLaboral.as_view()), name="historial_eliminar"),

    path('listar-areas/', login_required(AreaListView.as_view()), name='listarAreas'),
    path('crear-area/', login_required(AreaCreateView.as_view()), name='crearArea'),
    path('editar-area/<int:pk>/', login_required(AreaUpdateView.as_view()), name='editarArea'),

    path('listar-cargos/', login_required(CargoListView.as_view()), name='listarCargos'),
    path('crear-cargo/', login_required(CargoCreateView.as_view()), name='crearCargo'),
    path('editar-cargo/<int:pk>/', login_required(CargoUpdateView.as_view()), name='editarCargo'),

    path('listar-tipos-contrato/', login_required(TipoContratoListView.as_view()), name='listarTiposContrato'),
    path('crear-tipo-contrato/', login_required(TipoContratoCreateView.as_view()), name='crearTipoContrato'),
    path('editar-tipo-contrato/<int:pk>/', login_required(TipoContratoUpdateView.as_view()), name='editarTipoContrato'),

    path('listar-nombre-unidades/', login_required(NombreUnidadListView.as_view()), name='listarNombreUnidades'),
    path('crear-nombre-unidad/', login_required(NombreUnidadCreateView.as_view()), name='crearNombreUnidad'),
    path('editar-nombre-unidad/<int:pk>/', login_required(NombreUnidadUpdateView.as_view()), name='editarNombreUnidad'),

    path('utilidades-empleado/', login_required(UtilidadesProductos.as_view()), name='utilidadesEmpleado'),

]