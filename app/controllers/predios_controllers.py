from flask import Blueprint, request, jsonify
from firebase_admin import credentials, firestore, initialize_app
from datetime import datetime

predio_blue_print = Blueprint('app',__name__)

cred = credentials.Certificate('C:/Users/Said Aguilar/Documents/Proyecto Cabañas/Backend/data.json')
default_app = initialize_app(cred, {
    'databaseURL': 'https://datos.firebaseio.com'
})

db = firestore.client()
sap = db.collection('predios')

@predio_blue_print.route('/predios/register', methods=['POST'])
def create_predio():
    try:
        id_predio = request.json.get('id_predio')
        predio = request.json.get('predio')
        propietario = request.json.get('propietario')
        domicilio = request.json.get('domicilio')
        colonia = request.json.get('colonia')
        ref_ubicacion = request.json.get('ref_ubicacion')

        if not predio or not propietario or not domicilio or not colonia or not ref_ubicacion:
            return jsonify(warning = 'Los campos son requeridos'), 404

        sap.document(id_predio).set(request.json)
        return jsonify(response = 'Predio registrado correctamente'), 200
    except Exception as e:
        return f"An Error Occurred: {e}"


@predio_blue_print.route('/predio/listByPredio', methods=['POST','GET'])
def read_predios():
    current_date = datetime.now() 
    try:
        predio = request.json.get('predio')    

        if not predio:
            return jsonify(response = "Predio requerido"), 400
        
        collection = db.collection('registro_encuestado').where('predio', '==', predio)
        
        docs = []
        for doc in collection.stream():   
            formattedData = doc.to_dict()
            print(formattedData)
            docs.append(formattedData)
       
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

#TODO Se deben egenrar los metodos de actualizr y eliminar predio

@predio_blue_print.route('/predio/update', methods=['POST', 'PUT'])
def update_predio():
    try:
        id_predio = request.json.get('id_predio')
        sap.document(id_predio).update(request.json)
        return jsonify({"success": True}), 200
    except Exception as e:
        return f"An Error Occurred: {e}"
    

@predio_blue_print.route('/predio/delete', methods=['GET', 'DELETE'])
def delete_predio():
    try:
        # Check for ID in URL query
        id_predio = request.args.get('id_predio')
        sap.document(id_predio).delete()
        return jsonify({"success": True}), 200
    except Exception as e:
        return f"An Error Occurred: {e}"