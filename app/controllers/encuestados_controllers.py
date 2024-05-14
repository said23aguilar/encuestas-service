from flask import Blueprint, request, jsonify, flash
import firebase_admin
from firebase_admin import credentials, firestore, initialize_app

encuestados_blue_print = Blueprint('encuestados',__name__)

if not firebase_admin._apps:
    cred = credentials.Certificate('C:/Users/Said Aguilar/Documents/Proyecto Cabañas/Backend/data.json')
    default_app = initialize_app(cred, {
        'databaseURL': 'https://(default).firebaseio.com'
    })
db = firestore.client()
sap = db.collection('registro_encuestado')

@encuestados_blue_print.route('/encuestados/register', methods=['GET','POST'])
def create_predio():
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

        error = None

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
        
        if error is None:
            try:
                sap.document(predio).set(request.json)
                return jsonify(response = 'Encuestado registrado correctamente'), 200
            except Exception as e:
                return f"An Error Occurred: {e}"
        return jsonify(error = flash(error)), 404
    return jsonify(message = "No se pudo inciar el registro")
