"""Aplicación principal del microservicio Partner Lifecycle Management

En este archivo se define la aplicación principal del microservicio
"""

from flask import Flask
from partner_lifecycle.config.db import init_db
import os
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_app():
    app = Flask(__name__)
    
    # Configuración de la base de datos
    database_url = os.getenv('DATABASE_URL', 'postgresql://user:password@localhost:5432/partner_lifecycle')
    app.config['SQLALCHEMY_DATABASE_URI'] = database_url
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Inicializar base de datos
    init_db(app)
    
    # Importar handlers de comandos para registrar los dispatchers
    try:
        from partner_lifecycle.modulos.partner_lifecycle.aplicacion.handlers import crear_partnership_handler
        logger.info("Handlers de partner lifecycle registrados")
    except Exception as e:
        logger.error(f"Error registrando handlers de partner lifecycle: {e}")
    
    try:
        from partner_lifecycle.api.partner_lifecycle import bp as partner_lifecycle_bp
        app.register_blueprint(partner_lifecycle_bp)
        logger.info("Blueprint de partner lifecycle registrado")
    except Exception as e:
        logger.error(f"Error registrando blueprint de partner lifecycle: {e}")
    
    # Inicializar servicios de Pulsar (opcional)
    try:
        from partner_lifecycle.infraestructura.event_consumer_service import event_consumer_service
        from partner_lifecycle.infraestructura.pulsar import pulsar_publisher
        import atexit
        
        # Iniciar el servicio de consumo de eventos
        event_consumer_service.start_consuming()
        logger.info("Servicio de consumo de eventos iniciado")
        
        # Registrar función de limpieza al cerrar la aplicación
        atexit.register(cleanup_pulsar_connections)
        
    except Exception as e:
        logger.warning(f"Pulsar no disponible, continuando sin eventos: {e}")
    
    return app

def cleanup_pulsar_connections():
    """Limpia las conexiones de Pulsar al cerrar la aplicación"""
    try:
        from partner_lifecycle.infraestructura.event_consumer_service import event_consumer_service
        from partner_lifecycle.infraestructura.pulsar import pulsar_publisher
        event_consumer_service.stop_consuming()
        pulsar_publisher.close()
        logger.info("Conexiones de Pulsar cerradas correctamente")
    except Exception as e:
        logger.error(f"Error cerrando conexiones de Pulsar: {e}")

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5002)
