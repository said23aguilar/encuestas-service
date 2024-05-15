import os
from flask import Blueprint, request, jsonify, flash
import firebase_admin
from firebase_admin import credentials, firestore, initialize_app
from datetime import datetime
import json
from pywe_decrypt.msg import decrypt

encuestados_blue_print = Blueprint('encuestados',__name__)

json_account = {
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
    cred = credentials.Certificate(json_account)
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


