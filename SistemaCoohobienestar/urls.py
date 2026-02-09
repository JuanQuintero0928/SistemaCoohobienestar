"""
URL configuration for SistemaCoohobienestar project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import logout_then_login, LogoutView
from django.conf import settings
from django.conf.urls.static import static
from django.http import HttpResponse
from django.urls import path
from dashboard.views import Dashboard
from usuarios.views import CustomLoginView


# Función para manejar el chequeo de salud
def health_check(request):
    return HttpResponse("OK", status=200)

urlpatterns = [
    path('cooho-admin/', admin.site.urls),
    path('accounts/login/', CustomLoginView.as_view(template_name='registration/login.html'), name='login'),
    path('health/', health_check, name='health_check'),
    # path('logout/', logout_then_login, name='logout'),
    path('logout/admin/', LogoutView.as_view(next_page='/accounts/login/'), name='logout_admin'),
    path('logout/asociado/', LogoutView.as_view(next_page='/accounts/loginAsociado/'), name='logout_asociado'),
    path('', login_required(Dashboard.as_view()), name='dashboard'),
    path('informacion/', include(('dashboard.urls','informacion'))),  #Plantilla Principal de la base
    path('informacion/', include(('asociado.urls','asociado'))),
    path('informacion/', include(('beneficiario.urls','beneficiario'))),
    path('departamento/', include(('departamento.urls','departamento'))),
    path('parametro/', include(('parametro.urls','parametro'))),
    path('proceso/', include(('historico.urls','proceso'))),
    path('reportes/', include(('reportes.urls','reportes'))),
    path('ventas/', include(('ventas.urls','ventas'))),
    path('accounts/', include(('usuarios.urls','usuarios'))),
    path('perfil/', include(('perfil.urls','perfil'))),
    path('talento-humano/', include(('talento_humano.urls','talento_humano'))),
    # API
    path('api/', include('asociado.api.urls')),
    path('api/', include('usuarios.api.urls')),
    # UTILS
    path('parametro/utils/', include('parametro.utils.urls')),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
