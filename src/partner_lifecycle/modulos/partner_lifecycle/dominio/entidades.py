"""Entidades del dominio de Partner Lifecycle Management

En este archivo se definen las entidades del dominio para la gestión del ciclo de vida de partners

"""

from dataclasses import dataclass, field
from enum import Enum
from partner_lifecycle.seedwork.dominio.entidades import AgregacionRaiz
from partner_lifecycle.seedwork.dominio.eventos import EventoDominio
from datetime import datetime
import uuid

class EstadoPartnership(Enum):
    INICIANDO = "iniciando"
    EN_NEGOCIACION = "en_negociacion"
    ACTIVO = "activo"
    SUSPENDIDO = "suspendido"
    TERMINADO = "terminado"
    RENOVADO = "renovado"

class TipoPartnership(Enum):
    MARCA_AFILIADO = "marca_afiliado"
    MARCA_INFLUENCER = "marca_influencer"
    MARCA_EMBAJADOR = "marca_embajador"
    MARCA_SOCIO_B2B = "marca_socio_b2b"
    AFILIADO_INFLUENCER = "afiliado_influencer"
    INFLUENCER_EMBAJADOR = "influencer_embajador"

class NivelPartnership(Enum):
    BRONCE = "bronce"
    PLATA = "plata"
    ORO = "oro"
    PLATINO = "platino"
    DIAMANTE = "diamante"

@dataclass
class Partnership(AgregacionRaiz):
    id_marca: uuid.UUID = field(default=None)
    id_partner: uuid.UUID = field(default=None)
    tipo_partnership: TipoPartnership = field(default=None)
    estado: EstadoPartnership = field(default=EstadoPartnership.INICIANDO)
    nivel: NivelPartnership = field(default=NivelPartnership.BRONCE)
    fecha_inicio: datetime = field(default_factory=datetime.now)
    fecha_fin: datetime = field(default=None)
    fecha_ultima_actividad: datetime = field(default_factory=datetime.now)
    terminos_contrato: str = field(default="")
    comision_porcentaje: float = field(default=0.0)
    metas_mensuales: int = field(default=0)
    beneficios_adicionales: str = field(default="")
    notas: str = field(default="")
    
    def iniciar_negociacion(self, terminos: str = ""):
        if self.estado == EstadoPartnership.INICIANDO:
            self.estado = EstadoPartnership.EN_NEGOCIACION
            self.terminos_contrato = terminos
            self.fecha_ultima_actividad = datetime.now()
            self.agregar_evento(PartnershipIniciada(
                id_partnership=self.id,
                id_marca=self.id_marca,
                id_partner=self.id_partner,
                tipo_partnership=self.tipo_partnership.value,
                fecha_inicio=datetime.now()
            ))
    
    def activar_partnership(self, comision: float = 0.0, metas: int = 0):
        if self.estado == EstadoPartnership.EN_NEGOCIACION:
            self.estado = EstadoPartnership.ACTIVO
            self.comision_porcentaje = comision
            self.metas_mensuales = metas
            self.fecha_ultima_actividad = datetime.now()
            self.agregar_evento(PartnershipActivada(
                id_partnership=self.id,
                id_marca=self.id_marca,
                id_partner=self.id_partner,
                comision_porcentaje=comision,
                metas_mensuales=metas,
                fecha_activacion=datetime.now()
            ))
    
    def suspender_partnership(self, motivo: str = ""):
        if self.estado == EstadoPartnership.ACTIVO:
            self.estado = EstadoPartnership.SUSPENDIDO
            self.fecha_ultima_actividad = datetime.now()
            self.agregar_evento(PartnershipSuspendida(
                id_partnership=self.id,
                id_marca=self.id_marca,
                id_partner=self.id_partner,
                motivo=motivo,
                fecha_suspension=datetime.now()
            ))
    
    def terminar_partnership(self, motivo: str = ""):
        if self.estado in [EstadoPartnership.ACTIVO, EstadoPartnership.SUSPENDIDO]:
            self.estado = EstadoPartnership.TERMINADO
            self.fecha_fin = datetime.now()
            self.fecha_ultima_actividad = datetime.now()
            self.agregar_evento(PartnershipTerminada(
                id_partnership=self.id,
                id_marca=self.id_marca,
                id_partner=self.id_partner,
                motivo=motivo,
                fecha_terminacion=datetime.now()
            ))
    
    def renovar_partnership(self, nueva_fecha_fin: datetime, nuevos_terminos: str = ""):
        if self.estado == EstadoPartnership.ACTIVO:
            self.estado = EstadoPartnership.RENOVADO
            self.fecha_fin = nueva_fecha_fin
            if nuevos_terminos:
                self.terminos_contrato = nuevos_terminos
            self.fecha_ultima_actividad = datetime.now()
            self.agregar_evento(PartnershipRenovada(
                id_partnership=self.id,
                id_marca=self.id_marca,
                id_partner=self.id_partner,
                nueva_fecha_fin=nueva_fecha_fin,
                fecha_renovacion=datetime.now()
            ))
    
    def actualizar_nivel(self, nuevo_nivel: NivelPartnership):
        if self.estado == EstadoPartnership.ACTIVO and nuevo_nivel != self.nivel:
            nivel_anterior = self.nivel
            self.nivel = nuevo_nivel
            self.fecha_ultima_actividad = datetime.now()
            self.agregar_evento(NivelPartnershipActualizado(
                id_partnership=self.id,
                id_marca=self.id_marca,
                id_partner=self.id_partner,
                nivel_anterior=nivel_anterior.value,
                nivel_nuevo=nuevo_nivel.value,
                fecha_actualizacion=datetime.now()
            ))

@dataclass
class PartnershipIniciada(EventoDominio):
    id_partnership: uuid.UUID = None
    id_marca: uuid.UUID = None
    id_partner: uuid.UUID = None
    tipo_partnership: str = None
    fecha_inicio: datetime = None

@dataclass
class PartnershipActivada(EventoDominio):
    id_partnership: uuid.UUID = None
    id_marca: uuid.UUID = None
    id_partner: uuid.UUID = None
    comision_porcentaje: float = None
    metas_mensuales: int = None
    fecha_activacion: datetime = None

@dataclass
class PartnershipSuspendida(EventoDominio):
    id_partnership: uuid.UUID = None
    id_marca: uuid.UUID = None
    id_partner: uuid.UUID = None
    motivo: str = None
    fecha_suspension: datetime = None

@dataclass
class PartnershipTerminada(EventoDominio):
    id_partnership: uuid.UUID = None
    id_marca: uuid.UUID = None
    id_partner: uuid.UUID = None
    motivo: str = None
    fecha_terminacion: datetime = None

@dataclass
class PartnershipRenovada(EventoDominio):
    id_partnership: uuid.UUID = None
    id_marca: uuid.UUID = None
    id_partner: uuid.UUID = None
    nueva_fecha_fin: datetime = None
    fecha_renovacion: datetime = None

@dataclass
class NivelPartnershipActualizado(EventoDominio):
    id_partnership: uuid.UUID = None
    id_marca: uuid.UUID = None
    id_partner: uuid.UUID = None
    nivel_anterior: str = None
    nivel_nuevo: str = None
    fecha_actualizacion: datetime = None

@dataclass
class PartnershipCreationFailed(EventoDominio):
    id_partnership: uuid.UUID = None
    id_marca: uuid.UUID = None
    id_partner: uuid.UUID = None
    tipo_partnership: str = None
    fecha_inicio: datetime = None