import os
from flask import Blueprint, request, jsonify, flash
import firebase_admin
from firebase_admin import credentials, firestore, initialize_app
from datetime import datetime

encuestados_blue_print = Blueprint('encuestados',__name__)

if not firebase_admin._apps:
    cred = credentials.Certificate(os.getenv('SERVICE_ACCOUNT_FIREBASE'))
    default_app = initialize_app(cred, {
        'databaseURL': 'https://(default).firebaseio.com'
    })
db = firestore.client()
sap = db.collection('registro_encuestado')

@encuestados_blue_print.route('/encuestados/register', methods=['GET', 'PUT','POST'])
def create_encuestado():
    if request.method == 'POST':
        clave = request.json.get('clave')
        predio = request.json.get('predio')
        propietario = request.json.get('propietario')
        domicilio = request.json.get('domicilio')
        colonia = request.json.get('colonia')
        email = request.json.get('email')
        telefono = request.json.get('telefono')
        ref_ubicacion = request.json.get('ref_ubicacion')
        toma_agua = request.json.get('toma_agua')
        numero_tomas  = request.json.get('numero_tomas')
        ubicacion_toma = request.json.get('ubicacion_toma')
        medidor = request.json.get('medidor')
        nom_medidor = request.json.get('nom_medidor')
        ubicacion_medidor = request.json.get('ubicacion_medidor')
        estado_medidor = request.json.get('estado_medidor')
        referencia_ubicacion_medidor = request.json.get('nureferencia_ubicacion_medidormero_tomas')
        estado_toma = request.json.get('estado_toma')
        drenaje = request.json.get('drenaje')
        fosa_septica = request.json.get('fosa_septica')
        num_descargas = request.json.get('num_descargas')
        registro = request.json.get('registro')
        ubicacion_registro = request.json.get('ubicacion_registro')
        no_personas = request.json.get('no_personas')
        cisterna = request.json.get('cisterna')
        capacidad_cisterna = request.json.get('capacidad_cisterna')
        uso_cisterna = request.json.get('uso_cisterna')
        tinaco = request.json.get('tinaco')
        capacidad_tinaco = request.json.get('capacidad_tinaco')
        uso_tinaco = request.json.get('uso_tinaco')
        servicio_domestico = request.json.get('servicio_domestico')
        servicio_comercial = request.json.get('servicio_comercial')
        servicio_industrial = request.json.get('servicio_industrial')
        giro = request.json.get('giro')
        estado_vivienda = request.json.get('estado_vivienda')
        comentario_generales = request.json.get('comentario_generales')
        quien_proporciona_informacion = request.json.get('quien_proporciona_informacion')
        encuestadores = request.json.get('encuestadores')

        if not predio:
            return jsonify(response = 'Predio es requerido')
        elif not propietario:
            return jsonify(response = 'Propietario es requerido')
        elif not domicilio:
            return jsonify(response = 'Domicilio es requerido')
        elif not colonia:
            return jsonify(response = 'Colonia es requerido')
        elif not ref_ubicacion:
            return jsonify(response = 'Referencia Ubicacion es requerido')
        elif not toma_agua:
            return jsonify(response = 'Referencia toma_agua es requerido')
        elif not numero_tomas:
            return jsonify(response = 'Referencia numero_tomas es requerido')
        elif not ubicacion_toma:
            return jsonify(response = 'Referencia ubicacion_toma es requerido')
        elif not medidor:
            return jsonify(response = 'Referencia medidor es requerido')
        elif not nom_medidor:
            return jsonify(response = 'Referencia nom_medidor es requerido')
        elif not ubicacion_medidor:
            return jsonify(response = 'Referencia ubicacion_medidor es requerido')
        elif not estado_medidor:
            return jsonify(response = 'Referencia estado_medidor es requerido')
        elif not referencia_ubicacion_medidor:
            return jsonify(response = 'Referencia referencia_ubicacion_medidor es requerido')
        elif not estado_toma:
            return jsonify(response = 'Referencia estado_toma es requerido')
        elif not drenaje:
            return jsonify(response = 'Referencia drenaje es requerido')
        elif not fosa_septica:
            return jsonify(response = 'Referencia fosa_septica es requerido')
        elif not num_descargas:
            return jsonify(response = 'Referencia num_descargas es requerido')
        elif not registro:
            return jsonify(response = 'Referencia registro es requerido')
        elif not ubicacion_registro:
            return jsonify(response = 'Referencia ubicacion_registro es requerido')
        elif not no_personas:
            return jsonify(response = 'Referencia no_personas es requerido')
        elif not cisterna:
            return jsonify(response = 'Referencia cisterna es requerido')
        elif not capacidad_cisterna:
            return jsonify(response = 'Referencia capacidad_cisterna es requerido')
        elif not uso_cisterna:
            return jsonify(response = 'Referencia uso_cisterna es requerido')
        elif not tinaco:
            return jsonify(response = 'Referencia tinaco es requerido')
        elif not capacidad_tinaco:
            return jsonify(response = 'Referencia capacidad_tinaco es requerido')
        elif not uso_tinaco:
            return jsonify(response = 'Referencia uso_tinaco es requerido')
        elif not servicio_domestico:
            return jsonify(response = 'Referencia servicio_domestico es requerido')
        elif not servicio_comercial:
            return jsonify(response = 'Referencia servicio_comercial es requerido')
        elif not servicio_industrial:
            return jsonify(response = 'Referencia servicio_industrial es requerido')
        elif not giro:
            return jsonify(response = 'Referencia giro es requerido')
        elif not estado_vivienda:
            return jsonify(response = 'Referencia estado_vivienda es requerido')
        elif not comentario_generales:
            return jsonify(response = 'Referencia comentario_generales es requerido')
        elif not quien_proporciona_informacion:
            return jsonify(response = 'Referencia quien_proporciona_informacion es requerido')
        elif not encuestadores:
            return jsonify(response = 'Referencia encuestadores es requerido')
        

        try:
            sap.document(predio).set(request.json)
            print(request.json)
            return jsonify(response = 'Encuestado registrado correctamente'), 200
        except Exception as e:
            return jsonify(error = e)
    # Metodo para actualizar las credenciales de predio y capturar
    # if request.method == 'PUT':
    return jsonify(message = "No se pudo inciar el registro"), 400

@encuestados_blue_print.route('/encuestados/listByPredio', methods=['POST','GET'])
def read_encuestados():
    current_date = datetime.now() 
    try:
        predio = request.json.get('predio')    

        if not predio:
            return jsonify(response = "Predio requerido"), 400
        
        collection = db.collection('registro_encuestado').where('predio', '==', predio)
        
        docs = []
        for doc in collection.stream():   
            formattedData = doc.to_dict()
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
