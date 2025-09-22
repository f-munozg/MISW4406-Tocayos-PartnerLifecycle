"""Comandos para la gestión del ciclo de vida de partners

En este archivo se definen los comandos para la gestión del ciclo de vida de partners

"""

from dataclasses import dataclass
from partner_lifecycle.seedwork.aplicacion.comandos import Comando
from partner_lifecycle.modulos.partner_lifecycle.dominio.entidades import TipoPartnership, EstadoPartnership, NivelPartnership
from datetime import datetime
import uuid

@dataclass
class CrearPartnership(Comando):
    id: str
    saga_id: str
    id_marca: str
    id_partner: str
    tipo_partnership: str
    terminos_contrato: str = ""
    comision_porcentaje: float = 0.0
    metas_mensuales: int = 0
    beneficios_adicionales: str = ""
    notas: str = ""
    fecha_creacion: str = ""
    fecha_actualizacion: str = ""

@dataclass
class IniciarNegociacionPartnership(Comando):
    id_partnership: str
    terminos: str = ""
    fecha_actualizacion: str = ""

@dataclass
class ActivarPartnership(Comando):
    id_partnership: str
    comision_porcentaje: float = 0.0
    metas_mensuales: int = 0
    fecha_actualizacion: str = ""

@dataclass
class SuspenderPartnership(Comando):
    id_partnership: str
    motivo: str = ""
    fecha_actualizacion: str = ""

@dataclass
class TerminarPartnership(Comando):
    id_partnership: str
    motivo: str = ""
    fecha_actualizacion: str = ""

@dataclass
class RenovarPartnership(Comando):
    id_partnership: str
    nueva_fecha_fin: str
    nuevos_terminos: str = ""
    fecha_actualizacion: str = ""

@dataclass
class ActualizarNivelPartnership(Comando):
    id_partnership: str
    nuevo_nivel: str
    fecha_actualizacion: str = ""
