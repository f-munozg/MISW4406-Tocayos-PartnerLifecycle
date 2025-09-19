"""Servicio de Procesamiento de Eventos

En este archivo se define el servicio de aplicación para procesar eventos de dominio
siguiendo los principios de arquitectura hexagonal.

"""

from abc import ABC, abstractmethod
from typing import Dict, Any
import logging
from datetime import datetime
import uuid

logger = logging.getLogger(__name__)

class EventProcessingServiceInterface(ABC):
    """Interfaz para el servicio de procesamiento de eventos"""
    
    @abstractmethod
    def process_partnership_iniciada(self, payload: Dict[str, Any]) -> None:
        """Procesa el evento PartnershipIniciada"""
        pass

class EventProcessingService(EventProcessingServiceInterface):
    """Implementación del servicio de procesamiento de eventos"""
    
    def __init__(self, command_executor, app=None):
        self._command_executor = command_executor
        self._app = app
    
    def process_partnership_iniciada(self, payload: Dict[str, Any]) -> None:
        """Procesa el evento PartnershipIniciada ejecutando el comando CrearPartnership"""
        try:
            logger.info(f"Procesando PartnershipIniciada: {payload.get('id_partnership')}")
            
            # Mapear datos del evento a comando de aplicación
            command_data = self._map_partnership_iniciada_to_command(payload)
            
            # Ejecutar comando a través del executor con contexto de aplicación
            self._command_executor.execute_crear_partnership(command_data, self._app)
            
            logger.info(f"Comando CrearPartnership ejecutado exitosamente para partnership: {command_data['id']}")
            
        except Exception as e:
            logger.error(f"Error ejecutando CrearPartnership para partnership {payload.get('id_partnership')}: {e}")
            raise
    
    def _map_partnership_iniciada_to_command(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Mapea los datos del evento a los datos del comando"""
        return {
            'id': payload.get('id_partnership', str(uuid.uuid4())),
            'id_marca': payload.get('id_marca', str(uuid.uuid4())),
            'id_partner': payload.get('id_partner', str(uuid.uuid4())),
            'tipo_partnership': payload.get('tipo_partnership', 'marca_embajador'),
            'terminos_contrato': payload.get('terminos_contrato', ''),
            'comision_porcentaje': payload.get('comision_porcentaje', 0.0),
            'metas_mensuales': payload.get('metas_mensuales', 0),
            'beneficios_adicionales': payload.get('beneficios_adicionales', ''),
            'notas': payload.get('notas', ''),
            'fecha_creacion': datetime.now().isoformat(),
            'fecha_actualizacion': datetime.now().isoformat()
        }
