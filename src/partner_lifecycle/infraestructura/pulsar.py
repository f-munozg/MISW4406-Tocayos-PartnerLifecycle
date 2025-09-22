"""Configuración de Pulsar para eventos

En este archivo se define la configuración y utilidades para Pulsar

"""

import os
import json
import uuid
import logging
import pulsar
from typing import Dict, Any
from pulsar import Client, Producer, Consumer
from partner_lifecycle.seedwork.dominio.eventos import EventoDominio

# Try to import ConsumerType, fallback to string if not available
try:
    from pulsar import ConsumerType
except ImportError:
    # Fallback: use string values for consumer types
    class ConsumerType:
        Shared = "Shared"
        Exclusive = "Exclusive"
        Failover = "Failover"
        KeyShared = "KeyShared"

logger = logging.getLogger(__name__)

class PulsarConfig:
    def __init__(self):
        self.service_url = os.getenv('PULSAR_SERVICE_URL', 'pulsar://localhost:6650')
        self.admin_url = os.getenv('PULSAR_ADMIN_URL', 'http://localhost:8080')
        self.tenant = 'partner-lifecycle'
        self.namespace = 'events'
        
    def get_topic_name(self, event_type: str) -> str:
        """Genera el nombre del topic basado en el tipo de evento y tenant"""
        target_tenant = self.tenant
        if event_type.startswith('content'):
            target_tenant = 'content-management'
        return f"persistent://{target_tenant}/{self.namespace}/{event_type}"
    
    def get_routing_config(self, event_type: str, status: str) -> str:
        """Determina el tenant y topic basado en el tipo de evento y status"""
        if event_type == 'CommandCreatePartner' and status == 'failed':
            return 'content-events'
        elif event_type == 'EventPartnerCreated' and status == 'success':
            return 'partner-events'
        else:
            # Default routing
            return event_type

class PulsarEventPublisher:
    def __init__(self):
        self.config = PulsarConfig()
        self.client = None
        self.producers: Dict[str, Producer] = {}
        
    def _get_client(self) -> Client:
        """Obtiene o crea el cliente de Pulsar"""
        if self.client is None:
            self.client = Client(self.config.service_url)
        return self.client
    
    def _get_producer(self, topic_name: str) -> Producer:
        """Obtiene o crea un producer para el topic especificado"""
        if topic_name not in self.producers:
            client = self._get_client()
            self.producers[topic_name] = client.create_producer(topic_name)
        return self.producers[topic_name]
    
    def publish_event(self, evento: EventoDominio, event_type: str, status: str):
        """Publica un evento en Pulsar con routing basado en tipo y status"""
        try:
            # Determinar tenant y topic basado en el tipo de evento y status
            topic = self.config.get_routing_config(event_type, status)
            topic_name = self.config.get_topic_name(topic)
            producer = self._get_producer(topic_name)
            
            # Serializar el evento
            event_dict = {
                'saga_id': uuid.uuid4(),
                'service': 'Partner',
                'status': status, 
                'event_id': evento.id,
                'event_type': event_type,
                'event_data': evento.__dict__,
                'timestamp': evento.fecha_evento.isoformat() if hasattr(evento, 'fecha_evento') else None
            }
            event_data=json.dumps(event_dict, default=str)
            
            # Publicar el evento
            producer.send(event_data.encode('utf-8'))
            logger.info(f"Evento publicado en {topic_name} (topic: {topic}): {evento.__class__.__name__}")
            
        except Exception as e:
            logger.error(f"Error publicando evento en Pulsar: {e}")
            raise
    
    # def _serialize_event(self, evento: EventoDominio) -> str:
    #     """Serializa un evento a JSON"""
    #     event_dict = {
    #         'event_type': evento.__class__.__name__,
    #         'event_data': evento.__dict__,
    #         'timestamp': evento.fecha_evento.isoformat() if hasattr(evento, 'fecha_evento') else None
    #     }
    #     return json.dumps(event_dict, default=str)
    
    def close(self):
        """Cierra todas las conexiones"""
        for producer in self.producers.values():
            producer.close()
        if self.client:
            self.client.close()

class PulsarEventConsumer:
    def __init__(self):
        self.config = PulsarConfig()
        self.client = None
        self.consumers = {}
        
    def _get_client(self) -> Client:
        """Obtiene o crea el cliente de Pulsar"""
        if self.client is None:
            self.client = Client(self.config.service_url)
        return self.client
    
    def subscribe_to_topic(self, topic_name: str, subscription_name: str, callback):
        """Se suscribe a un topic específico"""
        try:
            client = self._get_client()
            consumer = client.subscribe(topic=topic_name, subscription_name=subscription_name, consumer_type=ConsumerType.Shared)
            self.consumers[topic_name] = consumer
            
            # Procesar mensajes en un hilo separado
            import threading
            thread = threading.Thread(target=self._process_messages, args=(consumer, callback))
            thread.daemon = True
            thread.start()
            
            logger.info(f"Suscrito al topic {topic_name} con subscription {subscription_name}")
            
        except Exception as e:
            logger.error(f"Error suscribiéndose al topic {topic_name}: {e}")
            raise
    
    def _process_messages(self, consumer, callback):
        """Procesa mensajes del consumer"""
        try:
            while True:
                try:
                    msg = consumer.receive(timeout_millis=1000)
                    # Deserializar el mensaje
                    event_data = json.loads(msg.data().decode('utf-8'))
                    callback(event_data)
                    consumer.acknowledge(msg)
                except Exception as e:
                    # Check if it's a timeout exception (normal behavior when no messages)
                    if "TimeOut" in str(e) or "timeout" in str(e).lower():
                        # This is normal - no messages available, continue waiting
                        continue
                    else:
                        # This is an actual error processing a message
                        logger.error(f"Error procesando mensaje: {e}")
                        if 'msg' in locals():
                            consumer.negative_acknowledge(msg)
        except Exception as e:
            logger.error(f"Error en el procesamiento de mensajes: {e}")
    
    def close(self):
        """Cierra todas las conexiones"""
        for consumer in self.consumers.values():
            consumer.close()
        if self.client:
            self.client.close()

# Instancia global del publisher
pulsar_publisher = PulsarEventPublisher()

# Instancia global del consumer
pulsar_consumer = PulsarEventConsumer()
