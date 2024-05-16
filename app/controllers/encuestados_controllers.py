import os
import firebase_admin
import json
from flask import Blueprint, request, jsonify
from firebase_admin import credentials, firestore, initialize_app
from datetime import datetime
from functools import wraps
from dotenv import load_dotenv

load_dotenv()

encuestados_blue_print = Blueprint('encuestados',__name__)

firebase_credentials = os.environ.get('SERVICE_ACCOUNT')

service_account= json.loads(firebase_credentials)


if not firebase_admin._apps:
    cred = credentials.Certificate(service_account)
    default_app = initialize_app(cred, {
        'databaseURL': 'https://(default).firebaseio.com'
    })
db = firestore.client()
sap = db.collection('registro_encuestado')

current_date = datetime.now() 

def check_required_fields(fields):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            missing_fields = [field for field in fields if not request.json.get(field)]
            if missing_fields:
                return jsonify(response = f'Los siguientes campos son requerios: {", ".join(missing_fields)}'), 400
            return func(*args, **kwargs)
        return wrapper
    return decorator

@encuestados_blue_print.route('/encuestados/register', methods=['POST'])
@check_required_fields([
        'clave', 'predio', 'propietario', 'domicilio', 'colonia', 'ref_ubicacion', 'toma_agua',
    'numero_tomas', 'ubicacion_toma', 'medidor', 'nom_medidor', 'ubicacion_medidor',
    'estado_medidor', 'referencia_ubicacion_medidor', 'estado_toma', 'drenaje', 
    'num_descargas', 'registro', 'ubicacion_registro', 'no_personas',
    'cisterna', 'capacidad_cisterna', 'uso_cisterna', 'tinaco', 'capacidad_tinaco',
    'uso_tinaco', 'servicio_domestico', 'servicio_comercial', 'servicio_industrial',
    'giro', 'estado_vivienda', 'comentario_generales', 'quien_proporciona_informacion',
    'encuestadores'
    ])
def create_encuestado():
    try:
        sap.document(request.json['predio']).set(request.json)
        return jsonify(response = 'Encuestdado registrado correctamente'), 201
    except Exception as e:
        return jsonify(error = str(e)), 500

@encuestados_blue_print.route('/encuestados/register', methods=['PUT'])
def update_encuestado():
    try:
        predio = request.json.get('predio')
        if not predio:
            return jsonify(response='El ID del predioes requerido'), 400
        sap.document(predio).update(request.json)
        return jsonify(reponse='Encuestado actualizado correctamente'), 200
    except Exception as e:
        return jsonify(error=str(e)), 500

@encuestados_blue_print.route('/encuestados/register', methods=['GET'])
def not_allowed():
    return jsonify(message="No se puede acceder a esta ruta con el metodo GET"), 405    

@encuestados_blue_print.route('/encuestados/list', methods=['GET'])
def read_encuestados_all():
    try:
        predio = request.args.get('predio')    
        if predio:
            todo = sap.document(predio).get()
            return jsonify(response = todo.to_dict()), 200
        else:
            all_todos = [doc.to_dict() for doc in sap.stream()]
            return jsonify(response = all_todos), 200
    except Exception as e:
        return jsonify( error = str(e)), 500

@encuestados_blue_print.route('/encuestados/listByPredio', methods=['POST','GET'])
def read_encuestados():
    try:
        predio = request.json.get('predio')    

        if not predio:
            return jsonify(response = "Predio requerido"), 400
        
        collection = db.collection('registro_encuestado').where('predio', '==', predio)
        
        docs = []
        for doc in collection.stream():   
            formatted_data = doc.to_dict()
            docs.append(formatted_data)
       
        if len(docs) == 0:
            error = {
                "status": 404,
                "title": "No se encontro ningun predio",
                "message": {
                    "predio": ["El predio no se pudo encontrar en la base de datos"]
                },
                "predio": predio,
                "timestamp": current_date

            }
            return jsonify(warning = error), 404
        return jsonify(response = docs), 200
    except Exception as e:
        return jsonify(error = e)

@encuestados_blue_print.route('/encuestado/delete', methods=['DELETE'])
def delete_predio():
    try:
        predio = request.args.get('predio')
        if not predio:
            error = {
                "status": 404,
                "title": "No se puede eliminar el predio",
                "message": {
                    "predio": ["El predio no se pudo eliminar"]
                },
                "timestamp": current_date
            }
            return jsonify( error = error), 404
        sap.document(predio).delete()
        return jsonify(response = f'Se elimino el predio: {predio} correctamente'), 200
    except Exception as e:
        return jsonify( error = str(e))
