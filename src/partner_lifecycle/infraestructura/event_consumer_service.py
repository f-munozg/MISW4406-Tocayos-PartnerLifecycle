"""Servicio de Consumo de Eventos

En este archivo se define el servicio principal para consumir eventos de Pulsar

"""

import json
import logging
import threading
from typing import Dict, Any
from partner_lifecycle.infraestructura.pulsar import PulsarEventConsumer, PulsarConfig

logger = logging.getLogger(__name__)

class EventConsumerService:
    def __init__(self, event_processing_service=None):
        self.config = PulsarConfig()
        self.consumers = {}
        self.running = False
        self._event_processing_service = event_processing_service
        
    def start_consuming(self):
        """Inicia el consumo de eventos para todos los módulos"""
        self.running = True
        
        # Eventos de partnerships
        self._start_consumer('partner-events', self._handle_partner_event)
        
        logger.info("Servicio de consumo de eventos iniciado")
    
    def stop_consuming(self):
        """Detiene el consumo de eventos"""
        self.running = False
        for consumer in self.consumers.values():
            consumer.close()
        logger.info("Servicio de consumo de eventos detenido")
    
    def _start_consumer(self, event_type: str, handler):
        """Inicia un consumidor para un tipo específico de evento"""
        try:
            consumer = PulsarEventConsumer()
            topic_name = self.config.get_topic_name(event_type)
            subscription_name = f"{event_type}-subscription"
            consumer.subscribe_to_topic(topic_name, subscription_name, handler)
            self.consumers[event_type] = consumer
            logger.info(f"Consumidor iniciado para {event_type}")
        except Exception as e:
            logger.error(f"Error iniciando consumidor para {event_type}: {e}")
    
    def _handle_partner_event(self, event_data: Dict[str, Any]):
        """Maneja eventos de partnerships"""
        try:
            event_type = event_data.get('event_type')
            event_payload = event_data.get('event_data', {})
            
            logger.info(f"Procesando evento de partnership: {event_type}")
            
            # Aquí se pueden agregar lógicas específicas para cada tipo de evento
            if event_type == 'PartnershipIniciada':
                self._process_partnership_iniciada(event_payload)
            elif event_type == 'PartnershipActivada':
                self._process_partnership_activada(event_payload)
            elif event_type == 'PartnershipSuspendida':
                self._process_partnership_suspendida(event_payload)
            elif event_type == 'PartnershipTerminada':
                self._process_partnership_terminada(event_payload)
                
        except Exception as e:
            logger.error(f"Error procesando evento de partnership: {e}")
    
    # Métodos de procesamiento específicos para cada evento
    def _process_partnership_iniciada(self, payload):
        """Procesa el evento PartnershipIniciada delegando a la capa de aplicación"""
        if self._event_processing_service:
            self._event_processing_service.process_partnership_iniciada(payload)
        else:
            logger.warning("EventProcessingService no configurado, solo logueando evento")
            logger.info(f"Partnership iniciada: {payload.get('id_partnership')}")
    
    def _process_partnership_activada(self, payload):
        logger.info(f"Partnership activada: {payload.get('id_partnership')}")
    
    def _process_partnership_suspendida(self, payload):
        logger.info(f"Partnership suspendida: {payload.get('id_partnership')}")
    
    def _process_partnership_terminada(self, payload):
        logger.info(f"Partnership terminada: {payload.get('id_partnership')}")

# Instancia global del servicio (se configurará con dependency injection)
event_consumer_service = None

def configure_event_consumer_service(event_processing_service):
    """Configura el servicio de consumo de eventos con dependency injection"""
    global event_consumer_service
    event_consumer_service = EventConsumerService(event_processing_service)
    return event_consumer_service
