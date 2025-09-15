"""Handler para el comando CrearPartnership

En este archivo se define el handler para crear partnerships

"""

from partner_lifecycle.modulos.partner_lifecycle.aplicacion.comandos.comandos_partnership import CrearPartnership
from partner_lifecycle.modulos.partner_lifecycle.infraestructura.modelos import (
    PartnershipDBModel, TipoPartnershipEnum, EstadoPartnershipEnum, NivelPartnershipEnum
)
from partner_lifecycle.seedwork.aplicacion.comandos import ejecutar_commando
from partner_lifecycle.infraestructura.pulsar import pulsar_publisher
from partner_lifecycle.config.db import db
from datetime import datetime
import uuid
import logging

logger = logging.getLogger(__name__)

@ejecutar_commando.register
def _(comando: CrearPartnership):
    """Handler para crear nueva partnership"""
    try:
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
        
        # Publicar evento en Pulsar
        pulsar_publisher.publish_event(evento, 'partner-events')
        
        logger.info(f"Partnership creada exitosamente: {partnership_model.id}")
        
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error creando partnership: {e}")
        raise
