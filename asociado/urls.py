from django.urls import path, include
from django.contrib.auth.decorators import login_required
from .views import *
from .utils.form_utils import actualizar_fecha_actualizacion
from ventas.views import ListarProductos, CrearProducto, EditarProducto, ListarVentasAsociado, CrearVentaAsociado, ListarDetalleVenta, EliminarDetalleVenta, UtilidadesProductos, verPagosVentas

urlpatterns = [
    path('asociado/', login_required(Asociados.as_view()), name='asociado'),
    path('crearAsociado/', login_required(CrearAsociado.as_view()), name='crearAsociado'),
    path('verAsociado/<int:pkAsociado>', login_required(VerAsociado.as_view()), name='verAsociado'),
    path('editarAsociado/<int:pkAsociado>', login_required(EditarAsociado.as_view()), name='editarAsociado'),
    path('editarLaboral/<int:pkAsociado>', login_required(EditarLaboral.as_view()), name='editarLaboral'),
    path('editarParametroAsociado/<int:pkAsociado>', login_required(EditarParametroAsociado.as_view()), name='editarParametroAsociado'),
    path('actualizarFechaActualizacion/<int:asociado_id>/', login_required(actualizar_fecha_actualizacion), name='actualizarFechaActualizacion'),

# Rutas de Beneficiarios
    path('beneficiario/<int:pkAsociado>', login_required(Beneficiarios.as_view()), name='beneficiario'),
    path('crearBeneficiario/<int:pkAsociado>', login_required(CrearBeneficiario.as_view()), name='crearBeneficiario'),
    path('editarBeneficiario/<int:pkAsociado>/<int:pk>', login_required(EditarBeneficiario.as_view()), name='editarBeneficiario'),
    path('eliminarBeneficiario/<int:pkAsociado>/<int:pk>', login_required(EliminarBeneficiario.as_view()), name='eliminarBeneficiario'),
    path('verBeneficiario/<int:pkAsociado>/<int:pk>', login_required(VerBeneficiario.as_view()), name='verBeneficiario'),

# Rutas de Mascotas
    path('mascota/<int:pkAsociado>', login_required(Mascotas.as_view()), name='mascota'),
    path('crearMascota/<int:pkAsociado>', login_required(CrearMascota.as_view()), name='crearMascota'),
    path('editarMascota/<int:pkAsociado>/<int:pk>', login_required(EditarMascota.as_view()), name='editarMascota'),    
    path('eliminarMascota/<int:pkAsociado>/<int:pk>', login_required(EliminarMascota.as_view()), name='eliminarMascota'),
    path('verMascota/<int:pkAsociado>/<int:pk>', login_required(VerMascota.as_view()), name='verMascota'),

# Rutas de Auxilios
    path('historicoAuxilio/<int:pkAsociado>', login_required(VerHistoricoAuxilio.as_view()), name='historicoAuxilio'),
    path('crearhistoricoAuxilio/<int:pkAsociado>', login_required(CrearAuxilio.as_view()), name='crearhistoricoAuxilio'),
    path('detalleAuxilio/<int:pkAsociado>/<int:pk>', login_required(DetalleAuxilio.as_view()), name='detalleAuxilio'),
    path('eliminarAuxilio/<int:pkAsociado>/<int:pk>', login_required(EliminarAuxilio.as_view()), name='eliminarAuxilio'),

# Rutas de Historico de Creditos
    path('historicoCredito/<int:pkAsociado>', login_required(VerHistoricoCredito.as_view()), name='historicoCredito'),
    path('verPagoshistoricoCredito/<int:pk>', login_required(verPagosCredito), name='verPagosHistoricoCredito'),
    path('crearHistoricoCredito/<int:pkAsociado>/', login_required(CrearHistoricoCredito.as_view()), name='crearHistoricoCredito'),
    path('editarHistoricoCredito/<int:pkAsociado>/<int:pk>', login_required(EditarHistoricoCredito.as_view()), name='editarHistoricoCredito'),
    
# Rutas de Tarifas y Adicionales
    path('tarifaAsociado/<int:pkAsociado>', login_required(VerTarifaAsociado.as_view()), name='tarifaAsociado'),
    path('crearAdicional/<int:pk>/', login_required(CrearAdicionalAsociado.as_view()), name='crearAdicional'),
    path('verAdicionalInactivo/<int:pk>', login_required(VerAdicionalAsociadoInactivo.as_view()), name='verAdicionalInactivo'),
    path('eliminarAdicional/<int:pkAsociado>/<int:pk>', login_required(EliminarAdicionalAsociado.as_view()), name='eliminarAdicional'),

# Rutas de Seguro de Vida
    path('seguroVida/<int:pkAsociado>', login_required(VerSeguroVida.as_view()), name='seguroVida'),
    path('crearSeguroVida/<int:pkAsociado>', login_required(CrearSeguroVida.as_view()), name='crearSeguroVida'),
    path('editarSeguroVida/<int:pkAsociado>/<int:pk>', login_required(EditarSeguroVida.as_view()), name='editarSeguroVida'),
    path('eliminarSeguroVida/<int:pkAsociado>/<int:pk>', login_required(EliminarSeguroVida.as_view()), name='eliminarSeguroVida'),
    path('VerSeguroVidaInactivo/<int:pkAsociado>/<int:pk>', login_required(VerSeguroVidaInactivo.as_view()), name='VerSeguroVidaInactivo'),

# Rutas de Coohoperativitos
    path('coohoperativitos/<int:pkAsociado>', login_required(VerCoohoperativitos.as_view()), name='coohoperativitos'),
    path('crearCoohoperativito/<int:pkAsociado>/', login_required(CrearCoohoperativito.as_view()), name='crearCoohoperativito'),
    path('editarCoohoperativito/<int:pkAsociado>/<int:pk>', login_required(EditarCoohoperativito.as_view()), name='editarCoohoperativito'),
    path('eliminarCoohoperativito/<int:pkAsociado>/<int:pk>', login_required(EliminarCoohoperativito.as_view()), name='eliminarCoohoperativito'),

# Rutas de Historico de Pagos
    path('historialPagos/<int:pkAsociado>', login_required(VerHistorialPagos.as_view()), name='historialPagos'),
    path('detallePago/<int:pkAsociado>/<int:pk>', login_required(DetalleHistorialPago.as_view()), name='detallePago'),
    path('descargarFormatos/<int:pkAsociado>', login_required(DescargarFormatos.as_view()), name='descargarFormatos'),
    path('modalFormato/<int:pkAsociado>/<int:formato>', login_required(ModalFormato.as_view()), name='modalFormato'),
    path('generarFormato/<int:pkAsociado>/<int:pk>/<int:formato>', login_required(GenerarFormato.as_view()), name='generarFormato'),
    path('utilidades', login_required(UtilidadesAsociado.as_view()), name='utilidades'),

# Rutas de Repatriación titular
    path('repatriacionTitular/<int:pkAsociado>', login_required(CrearRepatriacionTitular.as_view()), name='repatriacionTitular'),
    path('verRepatriacionTitular/<int:pk>/<int:pkAsociado>', login_required(VerRepatriacionTitular.as_view()), name='verRepatriacionTitular'),
    path('verRepatriacionTitularInactivo/<int:pk>/<int:pkAsociado>', login_required(VerRepatriacionTitularInactivo.as_view()), name='verRepatriacionTitularInactivo'),
    path('eliminarRepatriacionTitular/<int:pk>/<int:pkAsociado>', login_required(EliminarRepatriacionTitular.as_view()), name='eliminarRepatriacionTitular'),

# Rutas de Convenios
    path('crearConvenio/<int:pkAsociado>', login_required(CrearConvenio.as_view()), name='crearConvenio'),
    path('verConvenioAsociadoInactivo/<int:pk>/<int:pkAsociado>', login_required(VerConvenioAsociadoInactivo.as_view()), name='verConvenioAsociadoInactivo'),
    path('editarConvenio/<int:pkAsociado>/<int:pk>', login_required(EditarConvenioAsociado.as_view()), name='editarConvenio'),
    path('eliminarConvenio/<int:pkAsociado>/<int:pk>', login_required(EliminarConvenioAsociado.as_view()), name='eliminarConvenio'),
    path('verConvenioGasolina/<int:pkConvenio>/', login_required(EditarConvenioGasolina), name='verConvenioGasolina'),
    path('eliminar_detalle_gasolina/<int:pkConvenio>/', login_required(EliminarDetalleGasolina), name='eliminar_detalle_gasolina'),

# Rutas de Codeudores
    path('crearCodeudor/<int:pkAsociado>/<int:pk>', login_required(CrearCodeudor.as_view()), name='crearCodeudor'),
    path('editarCodeudor/<int:pk>/<int:pkAsociado>', login_required(EditarCodeudor.as_view()), name='editarCodeudor'),

# Vistas de la app Ventas
    path('listarProductos/', login_required(ListarProductos.as_view()), name='listarProductos'),
    path('crearProducto/', login_required(CrearProducto.as_view()), name='crearProducto'),
    path('editarProducto/<int:pk>', login_required(EditarProducto.as_view()), name='editarProducto'),
    path('listarVentasAsociado/<int:pkAsociado>', login_required(ListarVentasAsociado.as_view()), name='listarVentasAsociado'),
    path('verPagoshistoricoVenta/<int:pk>', login_required(verPagosVentas), name='verPagosHistoricoVenta'),

    path('crearVentaAsociado/<int:pkAsociado>', login_required(CrearVentaAsociado.as_view()), name='crearVentaAsociado'),
    path('detalleVenta/<int:pkAsociado>/<int:pk>', login_required(ListarDetalleVenta.as_view()), name='detalleVenta'),
    path('eliminarDetalleVenta/<int:pkAsociado>/<int:pk>', login_required(EliminarDetalleVenta.as_view()), name='eliminarDetalleVenta'),
    path('utilidadesProductos', login_required(UtilidadesProductos.as_view()), name='utilidadesProductos'),
]