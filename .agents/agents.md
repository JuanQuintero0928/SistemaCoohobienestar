# Contexto Técnico - Sistema Coohobienestar

## 1. Descripción General del Proyecto

Sistema de gestión cooperativa para la administración de asociados de Coohobienestar. Permite el registro, mantenimiento y seguimiento de asociados, incluyendo:

- Gestión de información personal y laboral de asociados
- Administración de beneficiarios (personas, mascotas, coohoperativitos)
- Control de tarifas y cuotas mensuales (aporte, bienestar social, adicionales)
- Gestión de créditos y auxilios económicos
- Seguimiento de pagos históricos
- Sistema de ventas de productos a asociados (crédito, descuento por nómina)
- Módulos de reportes y talento humano
- Portal de perfil para associado (autogestión)

## 2. Tecnologías Utilizadas

### Backend
- **Framework**: Django 5.0.6
- **Python**: 3.x
- **ORM**: Django ORM integrado

### Base de Datos
- **Motor**: PostgreSQL (configurado via `DATABASES` en settings.py)
- **Driver**: psycopg2-binary==2.9.9

### Frontend
- Templates HTML con Django Template Engine
- Bootstrap (sugerido por convención de clases CSS encontradas)
- JavaScript vanilla
- openpyxl para generación de archivos Excel

### Librerías Adicionales
- django-environ (configuración por entorno)
- djangorestframework (API REST)
- gunicorn (servidor WSGI)
- cement (CLI)
- openpyxl (exportación Excel)
- psutil (utilidades del sistema)

### Configuración
- Idioma: es-Co (español colombiano)

## 3. Estructura del Proyecto (Apps de Django)

| App | Propósito |
|-----|-----------|
| **asociado** | Gestión principal de asociados (datos personales, laboral, financiera, tarifas, repatriación, convenios) |
| **beneficiario** | Administración de beneficiarios (personas, mascotas, coohoperativitos) |
| **credito** | Gestión de codeudores para préstamos |
| **dashboard** | Panel principal con estadísticas de asociados |
| **departamento** | Catálogo geográfico (departamentos, municipios, países, indicativos) |
| **parametro** | Parámetros del sistema (tarifas, formas de pago, tipos de asociado, tasas de interés, consecutivos) |
| **historico** | Historial de auxilios, créditos, pagos y seguros de vida |
| **ventas** | Catálogo de productos y ventas a asociados |
| **reportes** | Módulos de generación de reportes Excel |
| **perfil** | Portal de autocuidado para asociados |
| **talento_humano** | Gestión de empleados, contratos, cargos |
| **usuarios** | Modelo personalizado de usuario (extiende AbstractUser) |

### Usuarios
- Extiende `AbstractUser` con `UsuarioAsociado`
- Relación uno a uno con modelo `Asociado`
- Campo `is_associate` para distinguir tipo de usuario

## 4. Arquitectura General

```
┌─────────────────────────────────────────────────────────────┐
│                    Django Project                        │
│                 SistemaCoohobienestar                  │
├─────────────────────────────────────────────────────────────┤
│  URL Routing (SistemaCoohobienestar/urls.py)           │
│  ├── /admin/ → Django Admin                          │
│  ├── /accounts/login/ → Autenticación              │
│  ├── /informacion/ → Dashboard, Asociados, etc.    │
│  ├── /departamento/ → Géografico                  │
│  ├── /parametro/ → Parámetros                 │
│  ├── /proceso/ → Pagos, Procesos              │
│  ├── /reportes/ → Reportes Excel                │
│  ├── /ventas/ → Productos y Ventas             │
│  ├── /accounts/ → Gestión usuarios             │
│  ├── /perfil/ → Portal asociado                │
│  ├── /talento-humano/ → RH                     │
│  └── /api/ → Endpoints REST                  │
├─────────────────────────────────────────────────────────────┤
│  Templates: templates/                           │
│  ├── estructura/ (head, navbar, sidebar, etc.) │
│  ├── base/ (vistas de asociados, etc.)          │
│  ├── reporte/ (reportes)                        │
│  ├── registration/ (login)                    │
│  └── ...                                     │
├─────────────────────────────────────────────────────────────┤
│  Database: PostgreSQL                           │
│  - asociado, beneficiario, credito,            │
│    dashboard, departamento, historico,         │
│    parametro, perfil, talento_humano, usuarios │
└─────────────────────────────────────────────────────────────┘
```

### Rutas Principales
- `/` → Dashboard (requiere login)
- `/accounts/login/` → Login de administrador
- `/informacion/asociado/` → Lista de asociados

## 5. Flujo Principal del Sistema

### Autenticación
1. Usuario `/accounts/login/`
2. Vista `CustomLoginView` procesa credenciales
3. Redirecciona a `/` (Dashboard) si es exitoso
4. Sesión dura 1 hora (`SESSION_COOKIE_AGE = 3600`)
5. Expira al cerrar navegador (`SESSION_EXPIRE_AT_BROWSER_CLOSE = True`)

### Gestión de Asociados
1. Crear asociado → datos personales, documento, ubicación
2. Editar asociado → información completa
3. Información laboral → empresa, cargo, контраto
4. Información financiera → ingresos/egresos
5. Tarifa asignada → cuotas mensuales
6. Beneficiarios → personas, mascotas, coohoperativitos
7. Estados: ACTIVO, INACTIVO, RETIRO

### Flujo de Pagos (HistorialPagos)
1. Registro de pagos mensuales por asociado
2. MesTarifa reference para control de períodos
3. Diferentes conceptos: aporte, bienestar social, mascota, repatriación, seguro vida, adicionales, coohoperativitos, convenio
4. Referencias a-credito: creditoId, ventaHE, convenio_gasolina_id

### Sistema de Créditos
1. Solicitud de crédito por asociado
2. Línea de crédito (anticipo nómina, credilibre, etc.)
3. Codeudor relacionado
4. Estado: REVISION, OTORGADO, DENEGADO
5. Historial de pagos asociado

### Reportes
- Exportación a Excel usando openpyxl
- Clases BaseReporteExcel con métodos estandarizados
- Parámetros por fecha

## 6. Convenciones Detectadas en el Código

### Nombres
- **Modelos**: PascalCase (e.g., `Asociado`, `HistoricoCredito`)
- **Vistas**: TipoApp (e.g., `Asociados`, `CrearAsociado`, `VerAsociado`)
- **URLs**: kebab-case (e.g., `crear-asociado`, `ver-asociado`)
- **Campos**: camelCase o snake_case inconsistente
- **Choices**: `tipoXxxOp` (e.g., `tipoDocumentoOp`, `generoOp`)
- **ForeignKey**: `modelo_id` o verbose_name

### Patrones
- Views basadas en `ListView`, `CreateView`, `UpdateView`, `DeleteView`
- Todas las vistas requieren `@login_required`
- Modelos con `estadoRegistro` booleano (soft delete)
- Campos de timestamps: `fechaCreacion`, `fechaModificacion`
- Choices como `TextChoices` anidados en modelos

### Organización
- Cada app tiene: models.py, views.py, urls.py, apps.py, admin.py
- Migrations en carpeta própria por app
- Templates en carpeta global `templates/`
- Archivos utilitarios en subcarpetas (utils/)

### Normalización
- Emails convertidos a minúsculas en save()
- Nombres convertidos a mayúsculas
- Longitudes de documento: max_length=11 (cédula) o 12

### API
- REST Framework instalado
- Endpoints en `/api/` via includes de apps
- Serializers separados en api/ dentro de cada app

## 7. Puntos Críticos y Áreas de Mejora

### Legibilidad y Mantenibilidad
1. **Campos con nombres ambiguos**: Algunos campos tienen nombres confusos (e.g., `primerMes`, `ultimoMes` referencias a MesTarifa)
2. **Choices inconsistentes**: Mezcla de convenciones (mayúsculas vs camelCase)
3. **Views muy largas**: Archivos como `reportes/views.py` con 1400+ líneas

### Base de Datos
4. **AutoField explícito**: Todos los modelos usan `id = models.AutoField(primary_key=True)` innecesario
5. **Constraints faltantes**: few unique constraints, no validaciones de integridad
6. **Índices**: No hay índices explícitos definidos

### Seguridad
7. **Hardcoded CSRF_TRUSTED_ORIGINS**: `appcoohobienestar.com` hardcoded en settings
8. **Validación de emails**: Solo lowercase, sin validación real de formato
9. **Sesión**: `SESSION_SAVE_EVERY_REQUEST = True` puede impactar rendimiento

### Código
10. **Comentarios mínimos**: Muy pocos comentarios docstring
11. **Duplicación**: Possible code duplication en modelos similares
12. **Utils dispersos**: Múltiples archivos utils (extracto.py, extracto_v1.py, etc.)

### Testing
13. **Tests vacíos**: Archivos tests.py existen pero sin implementación
14. **Sin coverage**: No hay configuración visible de coverage

### Variables de Entorno
15. **.env requerido**: El proyecto no funciona sin archivo .env con configuración

### frontend
16. **Templates dispersos**: Estructura de templates podría organizarse mejor
17. **CSS/JS**: static/ no encontrado, posible CSS inline

### Deprecaciones
18. **Múltiples versiones de utils**: Extracto v1, v2, v3 sugiere refactorings no completados
19. **Códigos comentados**: Several commented-out imports

### Administración
20. **Admin Django**: No se revisó configuración completa de admin.py


### Cómo contribuir al proyecto

- No modificar modelos sin migraciones
- Mantener consistencia en nombres
- Validar queries en vistas complejas

## Reglas del negocio

- Un asociado puede tener múltiples beneficiarios
- Los pagos están ligados a períodos (MesTarifa)
- Los créditos tienen estados definidos y flujo controlado

## Decisiones Técnicas

- Se utiliza Django con arquitectura basada en CBV (Class Based Views).
- Se implementa soft delete mediante el campo `estadoRegistro`.
- Se prioriza el uso del ORM de Django sobre consultas SQL directas.
- La lógica de negocio debe residir en modelos o servicios, no en templates.
- Se evita duplicación de lógica en múltiples apps.

## Comportamiento Esperado del Agente

- Debe analizar primero el contexto del proyecto antes de proponer soluciones.
- Debe respetar las reglas del negocio en todas las respuestas.
- Debe priorizar soluciones mantenibles sobre soluciones rápidas.
- Debe sugerir mejoras si detecta malas prácticas.
- Debe evitar respuestas genéricas y adaptarse a la arquitectura existente.
- Debe actuar como un desarrollador senior especializado en Django.

## Objetivo

Centralizar la gestión de asociados, pagos, créditos y beneficios en una plataforma única.

## Convenciones del proyecto

Actualmente el proyecto utiliza una mezcla de PascalCase y snake_case en nombres de campos.

Regla:
- No renombrar campos existentes en producción.
- Todo código nuevo debe usar snake_case.
- Mantener consistencia dentro de cada módulo.
---

*Documento generado automáticamente basándose en análisis del código fuente.*
*Última actualización: Abril 2026*