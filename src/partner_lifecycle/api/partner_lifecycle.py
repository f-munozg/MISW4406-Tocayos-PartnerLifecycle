"""API para la gestión del ciclo de vida de partners

En este archivo se define la API REST para la gestión del ciclo de vida de partners

"""

from flask import Blueprint, request, jsonify, Response
from partner_lifecycle.modulos.partner_lifecycle.aplicacion.comandos.comandos_partnership import (
    CrearPartnership, IniciarNegociacionPartnership, ActivarPartnership, 
    SuspenderPartnership, TerminarPartnership, RenovarPartnership, ActualizarNivelPartnership
)
from partner_lifecycle.seedwork.aplicacion.comandos import ejecutar_commando
from partner_lifecycle.seedwork.dominio.excepciones import ExcepcionDominio
from datetime import datetime
import json
import uuid
import logging

logger = logging.getLogger(__name__)

bp = Blueprint('partner_lifecycle', __name__, url_prefix='/partner-lifecycle')

@bp.route('/partnership', methods=['POST'])
def crear_partnership():
    try:
        partnership_dict = request.json
        logger.info(f"Request data: {partnership_dict}")
        
        #Nuevos mensajes 
        comando = CrearPartnership(
            id=partnership_dict.get('id', str(uuid.uuid4())),
            id_marca=partnership_dict.get('id_marca', str(uuid.uuid4())),
            id_partner=partnership_dict.get('id_identificacion', str(uuid.uuid4())),
            tipo_partnership=partnership_dict.get('tipo_partnership', 'marca_embajador'),
            terminos_contrato=partnership_dict.get('canales', ''),
            comision_porcentaje=partnership_dict.get('comision_porcentaje', 0.0),
            metas_mensuales=partnership_dict.get('metas_mensuales', 0),
            beneficios_adicionales=partnership_dict.get('campania_asociada', ''),
            notas=partnership_dict.get('categoria', ''),
            fecha_creacion=datetime.now().isoformat(),
            fecha_actualizacion=datetime.now().isoformat()
        )
        
        ejecutar_commando(comando)
        
        return Response('{}', status=202, mimetype='application/json')
    except ExcepcionDominio as e:
        return Response(json.dumps(dict(error=str(e))), status=400, mimetype='application/json')

@bp.route('/partnership/<id>/iniciar-negociacion', methods=['PUT'])
def iniciar_negociacion_partnership(id):
    try:
        data = request.json
        terminos = data.get('terminos', '') if data else ''
        
        comando = IniciarNegociacionPartnership(
            id_partnership=id,
            terminos=terminos,
            fecha_actualizacion=datetime.now().isoformat()
        )
        
        ejecutar_commando(comando)
        
        return Response('{}', status=202, mimetype='application/json')
    except ExcepcionDominio as e:
        return Response(json.dumps(dict(error=str(e))), status=400, mimetype='application/json')

@bp.route('/partnership/<id>/activar', methods=['PUT'])
def activar_partnership(id):
    try:
        data = request.json
        comision = data.get('comision_porcentaje', 0.0) if data else 0.0
        metas = data.get('metas_mensuales', 0) if data else 0
        
        comando = ActivarPartnership(
            id_partnership=id,
            comision_porcentaje=comision,
            metas_mensuales=metas,
            fecha_actualizacion=datetime.now().isoformat()
        )
        
        ejecutar_commando(comando)
        
        return Response('{}', status=202, mimetype='application/json')
    except ExcepcionDominio as e:
        return Response(json.dumps(dict(error=str(e))), status=400, mimetype='application/json')

@bp.route('/partnership/<id>/suspender', methods=['PUT'])
def suspender_partnership(id):
    try:
        data = request.json
        motivo = data.get('motivo', '') if data else ''
        
        comando = SuspenderPartnership(
            id_partnership=id,
            motivo=motivo,
            fecha_actualizacion=datetime.now().isoformat()
        )
        
        ejecutar_commando(comando)
        
        return Response('{}', status=202, mimetype='application/json')
    except ExcepcionDominio as e:
        return Response(json.dumps(dict(error=str(e))), status=400, mimetype='application/json')

@bp.route('/partnership/<id>/terminar', methods=['PUT'])
def terminar_partnership(id):
    try:
        data = request.json
        motivo = data.get('motivo', '') if data else ''
        
        comando = TerminarPartnership(
            id_partnership=id,
            motivo=motivo,
            fecha_actualizacion=datetime.now().isoformat()
        )
        
        ejecutar_commando(comando)
        
        return Response('{}', status=202, mimetype='application/json')
    except ExcepcionDominio as e:
        return Response(json.dumps(dict(error=str(e))), status=400, mimetype='application/json')

@bp.route('/partnership/<id>/renovar', methods=['PUT'])
def renovar_partnership(id):
    try:
        data = request.json
        nueva_fecha_fin = data.get('nueva_fecha_fin', '') if data else ''
        nuevos_terminos = data.get('nuevos_terminos', '') if data else ''
        
        comando = RenovarPartnership(
            id_partnership=id,
            nueva_fecha_fin=nueva_fecha_fin,
            nuevos_terminos=nuevos_terminos,
            fecha_actualizacion=datetime.now().isoformat()
        )
        
        ejecutar_commando(comando)
        
        return Response('{}', status=202, mimetype='application/json')
    except ExcepcionDominio as e:
        return Response(json.dumps(dict(error=str(e))), status=400, mimetype='application/json')

@bp.route('/partnership/<id>/actualizar-nivel', methods=['PUT'])
def actualizar_nivel_partnership(id):
    try:
        data = request.json
        nuevo_nivel = data.get('nuevo_nivel', 'bronce') if data else 'bronce'
        
        comando = ActualizarNivelPartnership(
            id_partnership=id,
            nuevo_nivel=nuevo_nivel,
            fecha_actualizacion=datetime.now().isoformat()
        )
        
        ejecutar_commando(comando)
        
        return Response('{}', status=202, mimetype='application/json')
    except ExcepcionDominio as e:
        return Response(json.dumps(dict(error=str(e))), status=400, mimetype='application/json')
