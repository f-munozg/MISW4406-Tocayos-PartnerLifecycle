# Partner Lifecycle Management Microservice

Este microservicio se encarga de la gestión del ciclo de vida de partnerships, incluyendo su creación, negociación, activación, suspensión, terminación y renovación.

## Características

- **Gestión de Partnerships**: Crear, negociar, activar, suspender, terminar y renovar partnerships
- **Tipos de Partnership**: Marca-Afilado, Marca-Influencer, Marca-Embajador, Marca-Socio B2B, Afiliado-Influencer, Influencer-Embajador
- **Estados**: Iniciando, En Negociación, Activo, Suspendido, Terminado, Renovado
- **Niveles**: Bronce, Plata, Oro, Platino, Diamante
- **Comisiones y Metas**: Gestión de comisiones por porcentaje y metas mensuales
- **Eventos**: Arquitectura orientada a eventos con Pulsar
- **Base de Datos**: PostgreSQL con SQLAlchemy

## Arquitectura

El microservicio sigue los principios de Domain-Driven Design (DDD) con:

- **Dominio**: Entidades, eventos de dominio y reglas de negocio
- **Aplicación**: Comandos, queries, handlers y DTOs
- **Infraestructura**: Modelos de base de datos, Pulsar, configuración
- **API**: Endpoints REST para operaciones CRUD

## Tecnologías

- **Backend**: Python 3.11, Flask
- **Base de Datos**: PostgreSQL 15
- **Eventos**: Apache Pulsar 3.1.0
- **ORM**: SQLAlchemy
- **Contenedores**: Docker, Docker Compose

## Instalación y Ejecución

### Con Docker Compose (Recomendado)

```bash
# Clonar el repositorio
git clone <repository-url>
cd partner-lifecycle

# Ejecutar con Docker Compose
docker-compose up -d

# El microservicio estará disponible en http://localhost:5002
```

### Desarrollo Local

```bash
# Instalar dependencias
pip install -r requirements.txt

# Configurar variables de entorno
export DATABASE_URL="postgresql://user:password@localhost:5432/partner_lifecycle"
export PULSAR_SERVICE_URL="pulsar://localhost:6650"
export PULSAR_ADMIN_URL="http://localhost:8080"

# Ejecutar la aplicación
python src/partner_lifecycle/main.py
```

## API Endpoints

### Partnerships

- `POST /partner-lifecycle/partnership` - Crear partnership
- `PUT /partner-lifecycle/partnership/{id}/iniciar-negociacion` - Iniciar negociación
- `PUT /partner-lifecycle/partnership/{id}/activar` - Activar partnership
- `PUT /partner-lifecycle/partnership/{id}/suspender` - Suspender partnership
- `PUT /partner-lifecycle/partnership/{id}/terminar` - Terminar partnership
- `PUT /partner-lifecycle/partnership/{id}/renovar` - Renovar partnership
- `PUT /partner-lifecycle/partnership/{id}/actualizar-nivel` - Actualizar nivel

## Eventos

El microservicio publica los siguientes eventos en Pulsar:

- `PartnershipIniciada` - Cuando se inicia una partnership
- `PartnershipActivada` - Cuando se activa una partnership
- `PartnershipSuspendida` - Cuando se suspende una partnership
- `PartnershipTerminada` - Cuando se termina una partnership
- `PartnershipRenovada` - Cuando se renueva una partnership
- `NivelPartnershipActualizado` - Cuando se actualiza el nivel

## Configuración

### Variables de Entorno

- `DATABASE_URL`: URL de conexión a PostgreSQL
- `PULSAR_SERVICE_URL`: URL del servicio Pulsar
- `PULSAR_ADMIN_URL`: URL del admin de Pulsar
- `FLASK_ENV`: Entorno de Flask (development/production)

### Base de Datos

El microservicio utiliza PostgreSQL con la siguiente estructura:

- **Tabla**: `partnerships`
- **Esquema**: `partner_lifecycle`
- **Índices**: Optimizados para consultas por marca, partner, estado y tipo

## Monitoreo

- **Pulsar Manager**: http://localhost:9529
- **Logs**: Disponibles en los contenedores Docker
- **Métricas**: A través de los eventos publicados en Pulsar

## Desarrollo

### Estructura del Proyecto

```
src/partner_lifecycle/
├── api/                    # Endpoints REST
├── config/                 # Configuración
├── infraestructura/        # Pulsar, base de datos
├── modulos/
│   └── partner_lifecycle/
│       ├── aplicacion/     # Comandos, queries, handlers
│       ├── dominio/        # Entidades, eventos
│       └── infraestructura/ # Modelos de BD
└── seedwork/              # Código reutilizable
```

### Agregar Nuevas Funcionalidades

1. **Dominio**: Definir entidades y eventos en `dominio/`
2. **Aplicación**: Crear comandos/queries en `aplicacion/`
3. **Infraestructura**: Implementar persistencia en `infraestructura/`
4. **API**: Exponer endpoints en `api/`

## Contribución

1. Fork el repositorio
2. Crear una rama para la funcionalidad
3. Hacer commit de los cambios
4. Crear un Pull Request

## Licencia

Este proyecto está bajo la licencia MIT.
