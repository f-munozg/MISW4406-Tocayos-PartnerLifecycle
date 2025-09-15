"""Modelos de base de datos para partnerships

En este archivo se definen los modelos de base de datos para partnerships

"""

from partner_lifecycle.config.db import db
from sqlalchemy import Column, String, DateTime, Float, Integer, Text, Enum
from sqlalchemy.dialects.postgresql import UUID
import uuid
from datetime import datetime
from enum import Enum as PyEnum

class TipoPartnershipEnum(PyEnum):
    MARCA_AFILIADO = "marca_afiliado"
    MARCA_INFLUENCER = "marca_influencer"
    MARCA_EMBAJADOR = "marca_embajador"
    MARCA_SOCIO_B2B = "marca_socio_b2b"
    AFILIADO_INFLUENCER = "afiliado_influencer"
    INFLUENCER_EMBAJADOR = "influencer_embajador"

class EstadoPartnershipEnum(PyEnum):
    INICIANDO = "iniciando"
    EN_NEGOCIACION = "en_negociacion"
    ACTIVO = "activo"
    SUSPENDIDO = "suspendido"
    TERMINADO = "terminado"
    RENOVADO = "renovado"

class NivelPartnershipEnum(PyEnum):
    BRONCE = "bronce"
    PLATA = "plata"
    ORO = "oro"
    PLATINO = "platino"
    DIAMANTE = "diamante"

class PartnershipDBModel(db.Model):
    __tablename__ = "partnerships"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    id_marca = Column(UUID(as_uuid=True), nullable=False)
    id_partner = Column(UUID(as_uuid=True), nullable=False)
    tipo_partnership = Column(Enum(TipoPartnershipEnum), nullable=False)
    estado = Column(Enum(EstadoPartnershipEnum), nullable=False, default=EstadoPartnershipEnum.INICIANDO)
    nivel = Column(Enum(NivelPartnershipEnum), nullable=False, default=NivelPartnershipEnum.BRONCE)
    fecha_inicio = Column(DateTime, nullable=False, default=datetime.utcnow)
    fecha_fin = Column(DateTime, nullable=True)
    fecha_ultima_actividad = Column(DateTime, nullable=False, default=datetime.utcnow)
    terminos_contrato = Column(Text, nullable=True)
    comision_porcentaje = Column(Float, nullable=False, default=0.0)
    metas_mensuales = Column(Integer, nullable=False, default=0)
    beneficios_adicionales = Column(Text, nullable=True)
    notas = Column(Text, nullable=True)
    fecha_creacion = Column(DateTime, nullable=False, default=datetime.utcnow)
    fecha_actualizacion = Column(DateTime, nullable=False, default=datetime.utcnow)
    
    def __repr__(self):
        return f"<Partnership {self.id_marca} - {self.id_partner} ({self.estado.value})>"
