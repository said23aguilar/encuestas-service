from flask import Marshmallow

ma = Marshmallow()

class PredioSchema(ma.Schema):

    class Meta:
        fields = ('id_predio', 'predio', 'propietario', 'domicilio', 'colonia', 'email', 'telefono', 'ref_ubicacion')

predio_schema = PredioSchema()
predios_schema = PredioSchema(many = True)