"""Handler para el comando CrearPartnership

En este archivo se define el handler para crear partnerships

"""

from partner_lifecycle.modulos.partner_lifecycle.aplicacion.comandos.comandos_partnership import CrearPartnership
from partner_lifecycle.modulos.partner_lifecycle.infraestructura.modelos import (
    PartnershipDBModel, TipoPartnershipEnum, EstadoPartnershipEnum, NivelPartnershipEnum
)
from partner_lifecycle.seedwork.aplicacion.comandos import ejecutar_commando
from partner_lifecycle.config.db import db

# Importar Pulsar solo si está disponible
try:
    from partner_lifecycle.infraestructura.pulsar import pulsar_publisher
    PULSAR_AVAILABLE = True
except ImportError:
    PULSAR_AVAILABLE = False
    pulsar_publisher = None
from datetime import datetime
import uuid
import logging

logger = logging.getLogger(__name__)

@ejecutar_commando.register
def _(comando: CrearPartnership):
    """Handler para crear nueva partnership"""
    evento = None  # Initialize evento variable
    partnership_model = None  # Initialize partnership_model variable
    
    try:

        if comando.id_marca == "c9b27e5f-5fa2-41bc-a539-1ce87d02a2f9":
            logger.error(f"Marca no permitida: {comando.id_marca} -> saga {comando.saga_id} -> pasando a rollback")
            raise Exception("Marca no permitida")

        # Crear modelo de base de datos directamente
        partnership_model = PartnershipDBModel()
        partnership_model.id = uuid.UUID(comando.id)
        partnership_model.id_marca = uuid.UUID(comando.id_marca)
        partnership_model.id_partner = uuid.UUID(comando.id_partner)
        partnership_model.tipo_partnership = TipoPartnershipEnum(comando.tipo_partnership)
        partnership_model.estado = EstadoPartnershipEnum.INICIANDO
        partnership_model.nivel = NivelPartnershipEnum.BRONCE
        partnership_model.terminos_contrato = comando.terminos_contrato
        partnership_model.comision_porcentaje = comando.comision_porcentaje
        partnership_model.metas_mensuales = comando.metas_mensuales
        partnership_model.beneficios_adicionales = comando.beneficios_adicionales
        partnership_model.notas = comando.notas
        
        if comando.fecha_creacion:
            partnership_model.fecha_creacion = datetime.fromisoformat(comando.fecha_creacion)
        if comando.fecha_actualizacion:
            partnership_model.fecha_actualizacion = datetime.fromisoformat(comando.fecha_actualizacion)
        
        # Guardar en base de datos
        db.session.add(partnership_model)
        db.session.commit()
        
        # Crear y publicar evento de dominio
        from partner_lifecycle.modulos.partner_lifecycle.dominio.entidades import PartnershipIniciada
        evento = PartnershipIniciada(
            id_partnership=partnership_model.id,
            id_marca=partnership_model.id_marca,
            id_partner=partnership_model.id_partner,
            tipo_partnership=partnership_model.tipo_partnership.value,
            fecha_inicio=partnership_model.fecha_creacion
        )
        
        if PULSAR_AVAILABLE and pulsar_publisher:
           pulsar_publisher.publish_event(comando.saga_id, evento, 'EventPartnerCompleted', 'success')
        else:
           logger.info("Pulsar no disponible, evento no publicado")
        
        logger.info(f"Partnership creada exitosamente: {partnership_model.id}")
        
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error creando partnership: {e}")
        
        # Only publish failure event if we have a valid partnership_model to create evento from
        if PULSAR_AVAILABLE and pulsar_publisher and partnership_model is not None:
            try:
                # Create appropriate failure event using the partnership_model if available
                from partner_lifecycle.modulos.partner_lifecycle.dominio.entidades import PartnershipCreationFailed
                evento = PartnershipCreationFailed(
                    id_partnership=partnership_model.id,
                    id_marca=partnership_model.id_marca,
                    id_partner=partnership_model.id_partner,
                    tipo_partnership=partnership_model.tipo_partnership.value,
                    fecha_inicio=partnership_model.fecha_creacion
                )
                pulsar_publisher.publish_event(comando.saga_id, evento, 'CommandCreatePartner', 'failed')
            except Exception as event_error:
                logger.error(f"Error creando evento de fallo: {event_error}")
        else:
           logger.info("Pulsar no disponible o partnership_model no disponible, evento no publicado")
        raise
