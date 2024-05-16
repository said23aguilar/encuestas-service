import os
from flask import Blueprint, request, jsonify
import firebase_admin
from firebase_admin import credentials, firestore, initialize_app
from datetime import datetime
from functools import wraps

encuestados_blue_print = Blueprint('encuestados',__name__)


service_account = {
    "type": "service_account",
    "project_id": "datos-64950",
    "private_key_id": "9ea2e16dba9ca06140cc6689846778ff72b63b98",
    "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQC2MgAGTZTMAXNv\nTc+MEF/iLzqIWXzwJOtaoll9nFRj44b8fzbCT9xS0IH59OsyJ/l9Siu0PaxQj0nB\n5X+vo45ClG9V+icDKhDuUZqEezXdUwErEFNk5gD95a8xtNSodthLjtigHyCfcE6G\nbFUiiammHS/oIvJs1IavIPUQ9HBHuT3a6ck4V+Xv64V21FEFQ5GbH5kLsCekbaGl\ntOJcwANg3IQ92NXTth9RBOmOCff5ndryaqdU75fGN9tBsvaWTuQlrXr1tJU66dPR\nGoZW3cnK21Y2th2M4/6Wbl4RHB5JlOGjToiTiFwAQ83ZjJawi0WfXgKYf0MKkFt3\nkifPvLclAgMBAAECggEAHvzZETlfveTfR8aBrs5YKIWk3Gzv+X4mA2fKdblBhy27\nFzXhz+G6VOF+wc8cs46l+d/EGCdHJ/p+7noEohBc0UkiuIpP2VNtxsLdV3wHOMn1\n0Ge571bJQ2WtyvP5GWABQLSednlk2IlG6ckCH9ovHwAm1kIfXlA1ShL+a3BPqnr3\nKdR3qGUgKRciu/7lslB/nsd5f7DluM57S7RIByy1F5xAZ2ucUqwZTcnxB5z0JHME\nrIXq17rUP3OSvlwg1lHXXF0UEdtw9ekOiKTCZUvG/1WT0v0oPcd6lFzVin5c42aR\nyqyfocDvRGgbMYNrhoqFbW+E2lHevzrTDUcFaGbHoQKBgQDYbnMNnoFMYgRJTPiF\nE3+lQ74N+2uRbobS9hT7rf7L6fDTMVKZOp5OWYtEgm0TFB7t++wmKvK/MLKk9aVu\nui+bN1PumdwiOIl2R+IPKcpHkRDUEiNAd4xJl7NTbKgyewGrLoTnTEI783XDUHoh\nnyRVPUxd3X/tV5rcUZ/moLkdUQKBgQDXgTYauKc9q6N2v7nKMa12j5oJCG1X63Yb\nT4eP+OjITDS24Oj0QeazxFV28Cr5AZSgYQMnFatn9azZMOXCUrr8CIiNLPJq3vYN\nmGUZx7VB6n8MEZp+qwkVT2dXUjjjNhZt7VHQ/q+H9Kh6AJbHqFy1PpMrff4JHSIR\noOLc0f53lQKBgQCFEXN/viK1OdZ00vRBrblffQUPR7PdWN1gO5ivHU15Rj6hOsQU\nHexTM87ismYpwsc5fxi0ZteVIXXU4otyRtsaTaw3GTY1fBlYNd4RgJoz4kc8fGJc\nMqR4YuMIude4IdTm0NU5+LMIdSnEimhs35HRLr0TQSp0XNaD+1Oa0tq94QKBgDAP\nyRk8hU/jr5kUOUM2wRDoBdpt3rT09mow2nLpeEDzfe4rSsjuyZzd9JGKDotqJtN9\nz04wLwIIcHwfw54LBVigLpQNqiLbhtSRYDrXpz0EJ0Fxy5rkWio+gzWeSMGjlmz9\nuHl703nmvow3BWmRyttBEWFpv/YYYTi9QNsuminhAoGAevJJX1jSvihXKeF28yvC\naVhPGmPbigKzWhnECcnpbcv+LsP+Wv9WlwWiKS50yLKjyWV/ZHwc5bjQRpl7frIa\nIV3NP+5baTaTlu7PuAYHwdrTAgyeaLo3X1CeGGbOKl3dFJd9mUQAJU8t4vvu4gjk\n4v5juuk5+pQ/6y43ELqYSsY=\n-----END PRIVATE KEY-----\n",
    "client_email": "firebase-adminsdk-ehb3n@datos-64950.iam.gserviceaccount.com",
    "client_id": "112399991812348544267",
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-ehb3n%40datos-64950.iam.gserviceaccount.com",
    "universe_domain": "googleapis.com"
}

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
    'fosa_septica', 'num_descargas', 'registro', 'ubicacion_registro', 'no_personas',
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
