"""Dependency Injection Container

En este archivo se define el contenedor de dependency injection para el módulo partner_lifecycle.

"""

from .event_processing_service import EventProcessingService
from .command_executor import CommandExecutor

class DependencyContainer:
    """Contenedor de dependencias para el módulo partner_lifecycle"""
    
    def __init__(self):
        self._command_executor = None
        self._event_processing_service = None
        self._app = None
    
    def set_app(self, app):
        """Establece la instancia de la aplicación Flask"""
        self._app = app
    
    def get_command_executor(self) -> CommandExecutor:
        """Obtiene la instancia del ejecutor de comandos"""
        if self._command_executor is None:
            self._command_executor = CommandExecutor()
        return self._command_executor
    
    def get_event_processing_service(self) -> EventProcessingService:
        """Obtiene la instancia del servicio de procesamiento de eventos"""
        if self._event_processing_service is None:
            command_executor = self.get_command_executor()
            self._event_processing_service = EventProcessingService(command_executor, self._app)
        return self._event_processing_service

# Instancia global del contenedor
dependency_container = DependencyContainer()
