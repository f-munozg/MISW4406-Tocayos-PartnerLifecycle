"""Ejecutor de Comandos

En este archivo se define el ejecutor de comandos para la capa de aplicación.

"""

from abc import ABC, abstractmethod
from typing import Dict, Any
import logging
from partner_lifecycle.modulos.partner_lifecycle.aplicacion.comandos.comandos_partnership import CrearPartnership
from partner_lifecycle.seedwork.aplicacion.comandos import ejecutar_commando

logger = logging.getLogger(__name__)

class CommandExecutorInterface(ABC):
    """Interfaz para el ejecutor de comandos"""
    
    @abstractmethod
    def execute_crear_partnership(self, command_data: Dict[str, Any], app=None) -> None:
        """Ejecuta el comando CrearPartnership"""
        pass

class CommandExecutor(CommandExecutorInterface):
    """Implementación del ejecutor de comandos"""
    
    def execute_crear_partnership(self, command_data: Dict[str, Any], app=None) -> None:
        """Ejecuta el comando CrearPartnership"""
        try:
            # Crear comando
            comando = CrearPartnership(**command_data)
            
            # Ejecutar comando con contexto de aplicación si está disponible
            if app:
                with app.app_context():
                    ejecutar_commando(comando)
            else:
                ejecutar_commando(comando)
            
        except Exception as e:
            logger.error(f"Error ejecutando comando CrearPartnership: {e}")
            raise
