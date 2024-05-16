import os
from flask import Blueprint, request, jsonify
from firebase_admin import credentials, firestore, initialize_app
from datetime import datetime
from models.predios_models import Predios
from dotenv import load_dotenv

load_dotenv()

predio_blue_print = Blueprint('app',__name__)


service_account= os.environ.get('SERVICE_ACCOUNT')

cred = credentials.Certificate(service_account)
default_app = initialize_app(cred, {
    'databaseURL': 'https://(default).firebaseio.com'
})

db = firestore.client()
sap = db.collection('predios')

current_date = datetime.now() 

@predio_blue_print.route('/predios/register', methods=['POST'])
def create_predio():
    try:
        id_predio = request.json.get('id_predio')
        predio = request.json.get('predio')
        propietario = request.json.get('propietario')
        domicilio = request.json.get('domicilio')
        colonia = request.json.get('colonia')
        ref_ubicacion = request.json.get('ref_ubicacion')
        serie_medidor = request.json.get('serie_medidor')

        if not predio or not propietario or not domicilio or not colonia or not ref_ubicacion or not serie_medidor:
            return jsonify(warning = 'Los campos son requeridos'), 404

        sap.document(id_predio).set(request.json)
        return jsonify(response = 'Predio registrado correctamente'), 200
    except Exception as e:
        return jsonify(error = e), 500

@predio_blue_print.route('/predio/list', methods=['GET'])
def read_predios_all():
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

@predio_blue_print.route('/predio/listByPredio', methods=['POST','GET'])
def read_predios():
    try:
        predio = request.json.get('predio')    
        if not predio:
            return jsonify(response = "Predio requerido"), 400
        
        collection = db.collection('predios').where('predio', '==', predio)
        
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


@predio_blue_print.route('/predio/update', methods=['POST', 'PUT'])
def update_predio():
    try:
        predio = request.json.get('predio')
        if not predio:
            error = {
                "status": 404,
                "title": "No se puede actualizar el predio",
                "message": {
                    "predio": ["El predio no se pudo actualizar"]
                },
                "timestamp": current_date
            }
            return jsonify( error = error), 404
        sap.document(predio).update(request.json)
        return jsonify(response = f'Se actualizo el predio {predio} correctamente'), 200
    except Exception as e:
        return jsonify( error = str(e))
    

@predio_blue_print.route('/predio/delete', methods=['GET', 'DELETE'])
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
    